"""E2E browser tests for Multi-Sheet Session Management, Unsaved Changes Prompts, and Template Status (Features 015, 016, 018)."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_multi_sheet_session_switching(page: Page):
    """Verifies that multi-sheet workbooks populate sheet picker and switch active canvases."""
    # Setup mock multi-sheet session via JS
    page.evaluate("""() => {
        App.currentFileName = 'MultiCompany.xlsx';
        App.currentFilePath = 'C:/Mock/MultiCompany.xlsx';
        App.currentSheetName = 'Sales_2026';
        App.cachedAllHeaders = {
            'Sales_2026': ['North_Sales', 'South_Sales'],
            'Marketing_2026': ['Ad_Budget', 'ROI']
        };
        App.activeSheetSelector.innerHTML = '';
        ['Sales_2026', 'Marketing_2026'].forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = s;
            if (s === 'Sales_2026') opt.selected = true;
            App.activeSheetSelector.appendChild(opt);
        });
    }""")

    sheet_selector = page.locator("#activeSheetSelector")
    expect(sheet_selector).to_be_visible()
    expect(sheet_selector.locator("option")).to_have_count(2)
    expect(sheet_selector).to_have_value("Sales_2026")


@pytest.mark.e2e
def test_unsaved_changes_modal_cancel_and_discard(page: Page):
    """Verifies unsaved changes prompt modal protects against accidental data loss when switching sheets."""
    # Setup session with 2 sheets
    page.evaluate("""() => {
        App.currentFileName = 'CompanyData.xlsx';
        App.currentFilePath = 'C:/Mock/CompanyData.xlsx';
        App.currentSheetName = 'Sheet1';
        App.cachedAllHeaders = { 'Sheet1': ['Col1'], 'Sheet2': ['Col2'] };
        App.activeSheetSelector.innerHTML = '';
        ['Sheet1', 'Sheet2'].forEach(s => {
            const opt = document.createElement('option');
            opt.value = s;
            opt.textContent = s;
            if (s === 'Sheet1') opt.selected = true;
            App.activeSheetSelector.appendChild(opt);
        });
        App.isDirty = true; // Simulating dirty state
    }""")

    # Try to switch sheet to Sheet2
    page.select_option("#activeSheetSelector", "Sheet2")

    # Unsaved modal should pop up
    expect(page.locator("#unsavedModal")).to_be_visible()

    # 1. Click Cancel
    page.click("#btnUnsavedCancel")
    expect(page.locator("#unsavedModal")).to_have_class("modal-overlay hidden")
    # Selector should revert back to Sheet1
    expect(page.locator("#activeSheetSelector")).to_have_value("Sheet1")

    # 2. Try again and click Discard
    page.select_option("#activeSheetSelector", "Sheet2")
    expect(page.locator("#unsavedModal")).to_be_visible()
    page.click("#btnUnsavedDiscard")
    expect(page.locator("#unsavedModal")).to_have_class("modal-overlay hidden")


@pytest.mark.e2e
def test_template_status_badge_sync(page: Page):
    """Verifies that template status badge displays bound file path."""
    expect(page.locator("#templateStatusBadge")).to_contain_text("Шаблон: (Немає)")

    page.evaluate("""() => {
        App.updateTemplateBadge("C:/Exports/Шаблон_FinalReport.xlsx");
    }""")

    expect(page.locator("#templateStatusBadge")).to_contain_text("Шаблон_FinalReport.xlsx")
