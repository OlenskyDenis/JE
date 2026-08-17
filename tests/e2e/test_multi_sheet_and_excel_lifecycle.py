"""E2E browser tests for Multi-Sheet Session Management, Unsaved Changes Prompts, and Template Status (Features 015, 016, 018)."""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_multi_sheet_session_switching(page: Page):
    """Verifies that multi-sheet workbooks populate sheet picker and switch active canvases."""
    # Setup multi-sheet session using SessionController public contract
    page.evaluate("""() => {
        SessionController.currentFileName = 'MultiCompany.xlsx';
        SessionController.currentTemplatePath = 'C:/Mock/MultiCompany.xlsx';
        SessionController.currentSheetName = 'Sales_2026';
        SessionController.cachedAllHeaders = {
            'Sales_2026': ['North_Sales', 'South_Sales'],
            'Marketing_2026': ['Ad_Budget', 'ROI']
        };
        SessionController.updateSheetSelectors(['Sales_2026', 'Marketing_2026'], 'Sales_2026');
    }""")

    sheet_selector = page.locator("#activeSheetSelector")
    expect(sheet_selector).to_be_visible()
    expect(sheet_selector.locator("option")).to_have_count(2)
    expect(sheet_selector).to_have_value("Sales_2026")


@pytest.mark.e2e
def test_unsaved_changes_modal_cancel_and_discard(page: Page):
    """Verifies unsaved changes prompt modal protects against accidental data loss when switching sheets."""
    sample_file = str(Path(__file__).parent.parent / "fixtures" / "excel_samples" / "multisheet_retail.xlsx")

    # Import real multi-sheet session
    page.evaluate(f"""async () => {{
        await SessionController.handleImportExcelFile({repr(sample_file)});
        SessionController.isDirty = true;
    }}""")

    # Try to switch sheet to Store_West
    page.select_option("#activeSheetSelector", "Store_West")

    # Unsaved modal should pop up
    expect(page.locator("#unsavedModal")).to_be_visible()

    # 1. Click Cancel
    page.click("#btnUnsavedCancel")
    expect(page.locator("#unsavedModal")).to_have_class("modal-overlay hidden")
    # Selector should revert back to Store_East
    expect(page.locator("#activeSheetSelector")).to_have_value("Store_East")

    # 2. Try again and click Discard
    page.select_option("#activeSheetSelector", "Store_West")
    expect(page.locator("#unsavedModal")).to_be_visible()
    page.click("#btnUnsavedDiscard")
    expect(page.locator("#unsavedModal")).to_have_class("modal-overlay hidden")
    # Verify active sheet actually switched to Store_West and isDirty is cleared
    expect(page.locator("#activeSheetSelector")).to_have_value("Store_West")
    is_dirty = page.evaluate("() => SessionController.isDirty")
    assert is_dirty is False

    # 3. Test Discard on Import Excel
    page.evaluate("() => { SessionController.isDirty = true; window._importOpened = false; SessionController.promptOpenAndImportFile = async () => { window._importOpened = true; }; }")
    page.click("#btnImportExcel")
    expect(page.locator("#unsavedModal")).to_be_visible()
    page.click("#btnUnsavedDiscard")
    expect(page.locator("#unsavedModal")).to_have_class("modal-overlay hidden")
    import_triggered = page.evaluate("() => window._importOpened")
    assert import_triggered is True, "Import was not triggered after clicking Discard!"


@pytest.mark.e2e
def test_template_status_badge_sync(page: Page):
    """Verifies that template status badge displays bound file path."""
    expect(page.locator("#templateStatusBadge")).to_contain_text("Шаблон: (Немає)")

    page.evaluate("""() => {
        SessionController.updateTemplateBadge("C:/Exports/Шаблон_FinalReport.xlsx");
    }""")

    expect(page.locator("#templateStatusBadge")).to_contain_text("Шаблон_FinalReport.xlsx")
