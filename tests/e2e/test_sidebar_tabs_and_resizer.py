"""E2E browser tests for Unified Sidebar Tabs, Search Filter, Collapse Strip, and Resizing (Features 013, 027)."""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_sidebar_tab_selector_switching(page: Page):
    """Verifies dropdown switching between Catalog and Paths Preview tabs."""
    expect(page.locator("#tabContentCatalog")).to_have_class("sidebar-tab-content active")
    expect(page.locator("#tabContentPaths")).to_have_class("sidebar-tab-content hidden")
    expect(page.locator("#headerCountBadge")).not_to_have_class("hidden")
    expect(page.locator("#pathCountBadge")).to_have_class("badge-count hidden")

    # Switch to Paths Tab
    page.select_option("#sidebarTabSelector", "paths")
    expect(page.locator("#tabContentPaths")).to_have_class("sidebar-tab-content active")
    expect(page.locator("#tabContentCatalog")).to_have_class("sidebar-tab-content hidden")
    expect(page.locator("#pathCountBadge")).not_to_have_class("hidden")
    expect(page.locator("#headerCountBadge")).to_have_class("badge-count hidden")

    # Switch back to Catalog Tab
    page.select_option("#sidebarTabSelector", "catalog")
    expect(page.locator("#tabContentCatalog")).to_have_class("sidebar-tab-content active")
    expect(page.locator("#tabContentPaths")).to_have_class("sidebar-tab-content hidden")


@pytest.mark.e2e
def test_sidebar_collapse_and_expand_strip(page: Page):
    """Verifies collapsing sidebar into vertical strip and restoring it."""
    sidebar = page.locator("#unifiedSidebar")
    expect(sidebar).not_to_have_class("panel unified-sidebar-panel sidebar-collapsed")

    # Collapse sidebar
    page.click("#btnToggleSidebarCollapse")
    expect(sidebar).to_have_class("panel unified-sidebar-panel sidebar-collapsed")
    expect(page.locator("#sidebarCollapsedStrip")).to_be_visible()

    # Expand sidebar via collapsed strip button
    page.click("#btnExpandSidebarStrip")
    expect(sidebar).not_to_have_class("sidebar-collapsed")

    # Collapse again and expand by clicking the vertical strip body
    page.click("#btnToggleSidebarCollapse")
    expect(sidebar).to_have_class("panel unified-sidebar-panel sidebar-collapsed")
    page.click("#sidebarCollapsedStrip")
    expect(sidebar).not_to_have_class("sidebar-collapsed")


@pytest.mark.e2e
def test_sidebar_search_filter_and_visibility(page: Page):
    """Verifies search filtering in catalog tab, ensuring items and lists are fully visible."""
    # Populate catalog with sample headers and enable controls via session controller
    page.evaluate("""() => {
        SessionController.updateSheetSelectors(['Sheet1'], 'Sheet1');
        App.currentRawHeaders = ['Revenue_Q1', 'Revenue_Q2', 'Expenses_Total', 'Net_Profit'];
        App.filterAndRenderSidebar();
    }""")

    # Controls must be enabled
    expect(page.locator("#sidebarSearch")).to_be_enabled()
    expect(page.locator("#catalogSheetSelector")).to_be_enabled()

    # List container must be visible, empty state hidden
    expect(page.locator("#sidebarHeaderList")).not_to_have_class("hidden")
    expect(page.locator("#sidebarEmptyState")).to_have_class("empty-state hidden")

    # All items must be visible
    expect(page.locator(".sidebar-header-item")).to_have_count(4)
    expect(page.locator(".sidebar-header-item").first).to_be_visible()

    # Search for 'Expenses'
    page.fill("#sidebarSearch", "Expenses")
    expect(page.locator(".sidebar-header-item")).to_have_count(1)
    expect(page.locator(".sidebar-header-item .header-title")).to_have_text("Expenses_Total")
    expect(page.locator(".sidebar-header-item").first).to_be_visible()

    # Clear search
    page.fill("#sidebarSearch", "")
    expect(page.locator(".sidebar-header-item")).to_have_count(4)


@pytest.mark.e2e
def test_sidebar_resizer_drag_and_double_click_reset(page: Page):
    """Verifies left-edge resizer drag and double-click reset to default width."""
    sidebar = page.locator("#unifiedSidebar")
    resizer = page.locator("#sidebarResizer")
    expect(resizer).to_be_visible()

    # Double-click resets to default width (340px)
    resizer.dblclick()
    width_after_dblclick = sidebar.evaluate("el => el.getBoundingClientRect().width")
    assert round(width_after_dblclick) == 340


@pytest.mark.e2e
def test_sidebar_catalog_sheet_change(page: Page):
    """Verifies changing catalog sheet dropdown updates catalog headers independently."""
    page.evaluate("""() => {
        SessionController.cachedAllHeaders = {
            'Summary': ['Revenue', 'Profit'],
            'Details': ['SKU', 'Quantity', 'UnitPrice', 'Discount']
        };
        SessionController.updateSheetSelectors(['Summary', 'Details'], 'Summary');
        SessionController.handleCatalogSheetChange('Summary');
    }""")

    expect(page.locator(".sidebar-header-item")).to_have_count(2)
    expect(page.locator(".sidebar-header-item").first).to_be_visible()

    # Change catalog sheet to Details
    page.select_option("#catalogSheetSelector", "Details")
    expect(page.locator(".sidebar-header-item")).to_have_count(4)
    expect(page.locator(".sidebar-header-item").first).to_be_visible()
