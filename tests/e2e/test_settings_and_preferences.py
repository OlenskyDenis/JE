"""E2E browser tests for Settings Modal, Delimiter Customization, and Reset to Defaults (Feature 026)."""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.conftest import add_child_node, create_root_node


@pytest.mark.e2e
def test_settings_modal_open_save_and_recalculation(page: Page):
    """Verifies opening settings modal, updating delimiter & default data type, and recalculating tree."""
    create_root_node(page, "Inventory", data_type="Text")
    add_child_node(page, "Inventory", "Stock", data_type="Integer")

    # Open Settings modal
    page.click("#btnSettings")
    expect(page.locator("#settingsModal")).to_be_visible()

    # Change delimiter from \ to /
    page.fill("#inputSettingDelimiter", "/")
    # Change default data type to Currency
    page.select_option("#selectSettingDefaultType", "Currency")

    # Save settings
    page.click("#btnSettingsSave")
    expect(page.locator("#settingsModal")).to_have_class("modal-overlay hidden")

    # Switch to Paths preview tab in sidebar to verify recalculated delimiter /
    page.select_option("#sidebarTabSelector", "paths")
    expect(page.locator("#pathList")).to_contain_text("Inventory/Stock")


@pytest.mark.e2e
def test_settings_reset_to_defaults(page: Page):
    """Verifies resetting settings restores standard delimiter and defaults."""
    # Open settings and customize
    page.click("#btnSettings")
    expect(page.locator("#settingsModal")).to_be_visible()

    page.fill("#inputSettingDelimiter", ";")
    page.click("#btnSettingsSave")

    # Re-open and reset to defaults
    page.click("#btnSettings")
    expect(page.locator("#settingsModal")).to_be_visible()
    expect(page.locator("#inputSettingDelimiter")).to_have_value(";")

    page.click("#btnSettingsReset")
    expect(page.locator("#settingsModal")).to_have_class("modal-overlay hidden")

    # Re-open to confirm reset
    page.click("#btnSettings")
    expect(page.locator("#inputSettingDelimiter")).to_have_value("\\")
    expect(page.locator("#selectSettingDefaultType")).to_have_value("Text")
    page.click("#btnSettingsCancel")
    expect(page.locator("#settingsModal")).to_have_class("modal-overlay hidden")
