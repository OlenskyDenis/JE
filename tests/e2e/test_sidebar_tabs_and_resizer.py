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


@pytest.mark.e2e
def test_sidebar_search_filter_with_headers(page: Page):
    """Verifies search filtering in catalog tab."""
    # Populate catalog with sample headers in JS
    page.evaluate("""() => {
        App.currentRawHeaders = ['Revenue_Q1', 'Revenue_Q2', 'Expenses_Total', 'Net_Profit'];
        App.filterAndRenderSidebar();
        document.getElementById('sidebarSearch').disabled = false;
    }""")

    expect(page.locator(".sidebar-header-item")).to_have_count(4)

    # Search for 'Expenses'
    page.fill("#sidebarSearch", "Expenses")
    expect(page.locator(".sidebar-header-item")).to_have_count(1)
    expect(page.locator(".sidebar-header-item .header-title")).to_have_text("Expenses_Total")

    # Clear search
    page.fill("#sidebarSearch", "")
    expect(page.locator(".sidebar-header-item")).to_have_count(4)
