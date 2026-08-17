"""Playwright E2E test configuration, live server fixture, and browser automation helpers."""

import os
import socket
import sys
import threading
import time
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

# Ensure repo root is on Python path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import eel

# Disable Eel's auto-shutdown on websocket disconnect during test session
eel._detect_shutdown = lambda *args, **kwargs: None

# Import bridge to register @eel.expose endpoints
import src.app.eel_bridge
from src.hierarchy_lib.services.settings_service import SettingsService


def get_free_port() -> int:
    """Finds an available TCP port for ephemeral server execution."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        s.listen(1)
        return s.getsockname()[1]


def wait_for_server(port: int, timeout: float = 6.0) -> bool:
    """Polls until local TCP server is listening."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return True
        except (OSError, ConnectionRefusedError):
            time.sleep(0.1)
    return False


@pytest.fixture(scope="session")
def eel_server_url() -> Generator[str, None, None]:
    """
    Session-scoped fixture that spins up the live Eel web application on an ephemeral port.
    """
    port = get_free_port()
    web_dir = os.path.join(REPO_ROOT, "src", "web")

    # Initialize Eel web folder
    eel.init(web_dir)

    # Start Eel web server in a daemon thread without auto-shutdown
    server_thread = threading.Thread(
        target=lambda: eel.start(
            "index.html", mode=False, port=port, block=True, host="127.0.0.1", shutdown_delay=999999
        ),
        daemon=True,
    )
    server_thread.start()

    if not wait_for_server(port, timeout=8.0):
        pytest.fail(f"Failed to start live Eel server on 127.0.0.1:{port}")

    url = f"http://127.0.0.1:{port}"
    yield url


@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    """Session-scoped Playwright browser instance."""
    is_headless = os.environ.get("HEADLESS", "0").lower() in ("1", "true", "yes")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=is_headless, slow_mo=30 if not is_headless else 0)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance: Browser, eel_server_url: str) -> Generator[Page, None, None]:
    """
    Function-scoped fixture providing a real, visual Chromium page context with isolated backend state.
    """
    # 1. Reset backend session state cleanly before each test
    src.app.eel_bridge.forest.root_nodes = []
    src.app.eel_bridge.sheet_forests.clear()
    src.app.eel_bridge.current_active_sheet = None
    src.app.eel_bridge.current_file_path = None
    src.app.eel_bridge.current_template_path = None
    SettingsService.reset_to_defaults()

    context: BrowserContext = browser_instance.new_context(
        viewport={"width": 1280, "height": 820}, ignore_https_errors=True
    )

    pg: Page = context.new_page()
    pg.goto(f"{eel_server_url}/index.html")
    pg.wait_for_selector(".app-container", state="visible", timeout=6000)

    yield pg

    # Close context cleanly per test
    context.close()


# ==============================================================================
# E2E Automation Action Helpers
# ==============================================================================


def create_root_node(page: Page, name: str, data_type: str = "Text") -> None:
    """Helper to create a root node via empty state button or header button."""
    if page.locator("#btnCreateRootEmpty").is_visible():
        page.click("#btnCreateRootEmpty")
    else:
        page.click("#btnAddRootHeader")

    page.wait_for_selector("#nodeModal:not(.hidden)", state="visible", timeout=3000)
    page.fill("#inputNodeName", name)
    if data_type and page.locator("#selectNodeType").is_visible():
        page.select_option("#selectNodeType", data_type)
    page.click("#btnModalSubmit")
    page.wait_for_selector(f".tree-node .node-title:has-text('{name}')", state="visible", timeout=4000)


def add_child_node(page: Page, parent_name: str, child_name: str, data_type: str = "Text") -> None:
    """Helper to add a child node to an existing parent node card."""
    node_content = page.locator(f".tree-node-content:has(.node-title:has-text('{parent_name}'))").first
    add_btn = node_content.locator(".action-btn.add-child").first
    add_btn.click()

    page.wait_for_selector("#nodeModal:not(.hidden)", state="visible", timeout=3000)
    page.fill("#inputNodeName", child_name)
    if data_type and page.locator("#selectNodeType").is_visible():
        page.select_option("#selectNodeType", data_type)
    page.click("#btnModalSubmit")
    page.wait_for_selector(f".tree-node .node-title:has-text('{child_name}')", state="visible", timeout=4000)
