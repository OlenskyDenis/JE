"""E2E browser tests for Navigation, Header Toolbar, and Bilingual Localization (Feature 031)."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_initial_page_load_and_branding(page: Page):
    """Verifies that the application loads with full header branding and toolbars."""
    expect(page.locator(".app-header")).to_be_visible()
    expect(page.locator(".brand h1")).to_be_visible()
    expect(page.locator("#btnImportExcel")).to_be_visible()
    expect(page.locator("#btnExportExcel")).to_be_visible()
    expect(page.locator("#btnRefresh")).to_be_visible()
    expect(page.locator("#btnSettings")).to_be_visible()
    expect(page.locator("#templateStatusBadge")).to_be_visible()


@pytest.mark.e2e
def test_bilingual_language_switcher_toggle(page: Page):
    """Verifies that toggling UA/EN re-translates all page titles, buttons, and badges in real-time."""
    # 1. Switch to English
    page.click("#langBtnEn")
    expect(page.locator("#langBtnEn")).to_have_class("lang-btn active")
    expect(page.locator(".brand h1")).to_have_text("Database Hierarchy Creator")
    expect(page.locator(".panel-header h2")).to_have_text("Hierarchy Constructor Workspace")
    expect(page.locator("#btnImportExcel span")).to_have_text("Import Excel")
    expect(page.locator("#btnExportExcel span")).to_have_text("Export Excel")
    expect(page.locator("#btnViewTree span")).to_have_text("Tree View")
    expect(page.locator("#btnViewMatrix span")).to_have_text("Excel Blocks")
    expect(page.locator("#btnViewUniqueLevels span")).to_have_text("Unique by Levels")

    # 2. Switch back to Ukrainian
    page.click("#langBtnUk")
    expect(page.locator("#langBtnUk")).to_have_class("lang-btn active")
    expect(page.locator(".brand h1")).to_have_text("Конструктор ієрархії баз даних")
    expect(page.locator(".panel-header h2")).to_have_text("Робоча область конструктора ієрархії")
    expect(page.locator("#btnImportExcel span")).to_have_text("Імпорт Excel")
    expect(page.locator("#btnExportExcel span")).to_have_text("Експорт Excel")
    expect(page.locator("#btnViewTree span")).to_have_text("Дерево")
    expect(page.locator("#btnViewMatrix span")).to_have_text("Блоки Excel")
    expect(page.locator("#btnViewUniqueLevels span")).to_have_text("Унікальні за рівнями")


@pytest.mark.e2e
def test_bilingual_modal_translation_parity(page: Page):
    """Verifies that modal dialogs and buttons update their translated strings on language switch."""
    # Open node modal in UK
    page.click("#btnAddRootHeader")
    expect(page.locator("#nodeModal")).to_be_visible()
    expect(page.locator("#modalTitle")).to_have_text("Створити вузол")
    page.click("#modalClose")

    # Switch to EN
    page.click("#langBtnEn")
    page.click("#btnAddRootHeader")
    expect(page.locator("#nodeModal")).to_be_visible()
    expect(page.locator("#modalTitle")).to_have_text("Create Node")
    page.click("#modalClose")


@pytest.mark.e2e
def test_refresh_workspace_button(page: Page):
    """Verifies that clicking the refresh session button functions without errors."""
    page.click("#btnRefresh")
    # Wait for tree empty state or tree container to be ready
    expect(page.locator("#treeEmptyState")).to_be_visible()


@pytest.mark.e2e
def test_toast_notifications_visual_styles_and_types(page: Page):
    """Verifies that all toast notification types (info, warning, success, error) render with non-transparent border and background."""
    types_to_test = ["info", "warning", "success", "error"]
    for t_type in types_to_test:
        page.evaluate(f"""() => {{
            App.showToast("Test toast {t_type}", "{t_type}");
        }}""")
        toast_el = page.locator(f".toast.toast-{t_type}").last
        expect(toast_el).to_be_visible()

        # Verify computed styles are not transparent
        bg_color = toast_el.evaluate("el => window.getComputedStyle(el).backgroundColor")
        border_width = toast_el.evaluate("el => window.getComputedStyle(el).borderWidth")
        border_style = toast_el.evaluate("el => window.getComputedStyle(el).borderStyle")

        assert bg_color != "rgba(0, 0, 0, 0)" and bg_color != "transparent"
        assert border_style == "solid"
        assert border_width != "0px"
