"""E2E browser tests for Drag-and-Drop Gestures, 3-Zone Highlights, and Cycle Prevention (Feature 031)."""

import pytest
from playwright.sync_api import Page, expect
from tests.e2e.conftest import create_root_node, add_child_node


@pytest.mark.e2e
def test_drag_and_drop_add_header_from_catalog(page: Page):
    """Verifies adding a header column into the tree via DragDrop payload handler."""
    create_root_node(page, "Categories", data_type="Text")
    
    parent_card = page.locator(".tree-node-content:has(.node-title:has-text('Categories'))").first
    target_id = parent_card.get_attribute("data-id")
    
    # Simulate dropping a new catalog item 'Revenue' inside 'Categories'
    page.evaluate(f"""() => {{
        App.handleDropPayload({{ isNew: true, label: 'Revenue', dataType: 'Currency' }}, '{target_id}', 'NEST_CHILD');
    }}""")
    
    # Verify child is created under Categories
    expect(page.locator(".tree-children .node-title:has-text('Revenue')")).to_be_visible()
    expect(page.locator(".tree-children .node-type-badge:has-text('Валюта')")).to_be_visible()


@pytest.mark.e2e
def test_reorder_nodes_before_and_after_zones(page: Page):
    """Verifies reordering sibling nodes via drop zones."""
    create_root_node(page, "FirstRoot", data_type="Text")
    create_root_node(page, "SecondRoot", data_type="Text")
    
    first_card = page.locator(".tree-node-content:has(.node-title:has-text('FirstRoot'))").first
    second_card = page.locator(".tree-node-content:has(.node-title:has-text('SecondRoot'))").first
    
    first_id = first_card.get_attribute("data-id")
    second_id = second_card.get_attribute("data-id")
    
    # Move SecondRoot before FirstRoot
    page.evaluate(f"""() => {{
        App.handleDropPayload({{ id: '{second_id}' }}, '{first_id}', 'BEFORE_SIBLING');
    }}""")
    
    # Verify order changed
    first_node_title = page.locator(".tree-node .node-title").first
    expect(first_node_title).to_have_text("SecondRoot")


@pytest.mark.e2e
def test_cycle_detection_prohibits_parent_into_child(page: Page):
    """Verifies that moving a parent into its own descendant is rejected with a warning."""
    create_root_node(page, "MainParent", data_type="Text")
    add_child_node(page, "MainParent", "SubChild", data_type="Text")
    
    parent_card = page.locator(".tree-node-content:has(.node-title:has-text('MainParent'))").first
    child_card = page.locator(".tree-node-content:has(.node-title:has-text('SubChild'))").first
    
    parent_id = parent_card.get_attribute("data-id")
    child_id = child_card.get_attribute("data-id")
    
    # Attempt illegal cycle: drop parent into its child
    page.evaluate(f"""() => {{
        App.handleDropPayload({{ id: '{parent_id}' }}, '{child_id}', 'NEST_CHILD');
    }}""")
    
    # Verify warning toast appears and structure is preserved
    expect(page.locator(".toast.toast-warning:has-text('Cannot move parent node')")).to_be_visible()
    expect(page.locator(".tree-node:has(.node-title:has-text('MainParent'))")).to_be_visible()
