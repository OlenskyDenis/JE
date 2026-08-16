"""E2E browser tests for Hierarchy Tree CRUD Operations, Folder Chevrons, and Modals (Feature 031)."""

import pytest
from playwright.sync_api import Page, expect
from tests.e2e.conftest import create_root_node, add_child_node


@pytest.mark.e2e
def test_create_root_node_and_modal_validation(page: Page):
    """Verifies creating a root node via empty state button and input validation."""
    expect(page.locator("#treeEmptyState")).to_be_visible()
    
    # Click create root button from empty state
    page.click("#btnCreateRootEmpty")
    expect(page.locator("#nodeModal")).to_be_visible()
    
    page.fill("#inputNodeName", "Root_A")
    page.select_option("#selectNodeType", "Text")
    page.click("#btnModalSubmit")
    
    expect(page.locator("#nodeModal")).to_have_class("modal-overlay hidden")
    expect(page.locator(".tree-node .node-title:has-text('Root_A')")).to_be_visible()
    expect(page.locator("#nodeCountBadge")).to_contain_text("1")


@pytest.mark.e2e
def test_add_child_nesting_and_folder_chevrons(page: Page):
    """Verifies child node nesting, folder transformation, and chevron collapse/expand."""
    create_root_node(page, "Sales", data_type="Text")
    add_child_node(page, "Sales", "Q1_Report", data_type="Currency")
    
    # Verify parent has folder icon and chevron
    parent_card = page.locator(".tree-node:has(.node-title:has-text('Sales'))").first
    expect(parent_card.locator(".node-icon.folder")).to_be_visible()
    expect(parent_card.locator(".node-toggle")).to_be_visible()
    
    # Verify child node has currency type badge
    child_card = parent_card.locator(".tree-children .tree-node:has(.node-title:has-text('Q1_Report'))").first
    expect(child_card.locator(".node-type-badge")).to_have_text("Валюта")
    
    # Test collapse chevron
    toggle_btn = parent_card.locator(".node-toggle").first
    toggle_btn.click()
    expect(parent_card).to_have_class("tree-node collapsed")
    expect(parent_card.locator(".tree-children")).not_to_be_visible()
    
    # Test expand chevron
    toggle_btn.click()
    expect(parent_card).to_have_class("tree-node")
    expect(parent_card.locator(".tree-children")).to_be_visible()


@pytest.mark.e2e
def test_toolbar_expand_all_and_collapse_all(page: Page):
    """Verifies global toolbar expand all and collapse all buttons."""
    create_root_node(page, "Dept", data_type="Text")
    add_child_node(page, "Dept", "Team", data_type="Text")
    add_child_node(page, "Team", "Member", data_type="Text")
    
    # Collapse all
    page.click("#btnCollapseAll")
    expect(page.locator(".tree-node.collapsed")).to_have_count(2)
    
    # Expand all
    page.click("#btnExpandAll")
    expect(page.locator(".tree-node.collapsed")).to_have_count(0)


@pytest.mark.e2e
def test_edit_node_modal_and_type_update(page: Page):
    """Verifies editing node name and changing data type via double-click and rename button."""
    create_root_node(page, "Price", data_type="Decimal")
    
    price_node = page.locator(".tree-node:has(.node-title:has-text('Price'))").first
    rename_btn = price_node.locator(".action-btn.rename-node").first
    rename_btn.click()
    
    expect(page.locator("#nodeModal")).to_be_visible()
    expect(page.locator("#inputNodeName")).to_have_value("Price")
    
    # Change name and type
    page.fill("#inputNodeName", "Total_Amount")
    page.select_option("#selectNodeType", "Currency")
    page.click("#btnModalSubmit")
    
    expect(page.locator(".tree-node .node-title:has-text('Total_Amount')")).to_be_visible()
    expect(page.locator(".tree-node .node-type-badge")).to_have_text("Валюта")


@pytest.mark.e2e
def test_delete_node_with_confirmation(page: Page):
    """Verifies deleting nodes with native dialog confirmation."""
    create_root_node(page, "TempNode", data_type="Text")
    expect(page.locator(".tree-node .node-title:has-text('TempNode')")).to_be_visible()
    
    # Accept delete confirmation dialog automatically
    page.on("dialog", lambda dialog: dialog.accept())
    
    node_card = page.locator(".tree-node:has(.node-title:has-text('TempNode'))").first
    delete_btn = node_card.locator(".action-btn.delete").first
    delete_btn.click()
    
    # Verify node is removed and empty state returns
    expect(page.locator(".tree-node .node-title:has-text('TempNode')")).not_to_be_visible()
    expect(page.locator("#treeEmptyState")).to_be_visible()
