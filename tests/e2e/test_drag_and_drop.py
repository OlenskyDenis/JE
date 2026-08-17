"""E2E browser tests for Drag-and-Drop Gestures, 3-Zone Highlights, and Cycle Prevention (Feature 031)."""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.conftest import add_child_node, create_root_node


@pytest.mark.e2e
def test_drag_and_drop_add_header_from_catalog(page: Page):
    """Verifies adding a header column from catalog into the tree via native Drag-and-Drop gesture."""
    sample_file = str(Path(__file__).parent.parent / "fixtures" / "excel_samples" / "standard_hierarchy.xlsx")

    # 1. Import file to populate sidebar catalog
    page.evaluate(f"async () => {{ await SessionController.handleImportExcelFile({repr(sample_file)}); }}")

    # Clear workspace tree to start clean
    create_root_node(page, "Categories", data_type="Text")

    catalog_item = page.locator(".sidebar-header-item:has-text('Price')").first
    target_node = page.locator(".tree-node-content:has(.node-title:has-text('Categories'))").first

    expect(catalog_item).to_be_visible()
    expect(target_node).to_be_visible()

    # Perform native drag and drop from sidebar catalog directly into target node card
    catalog_item.drag_to(target_node, target_position={"x": 60, "y": 20})

    # Verify child node 'Price' is created under Categories with proper badge
    expect(page.locator(".tree-children .node-title:has-text('Price')")).to_be_visible()
    expect(page.locator(".tree-children .node-type-badge")).to_be_visible()


@pytest.mark.e2e
def test_reorder_nodes_before_and_after_zones(page: Page):
    """Verifies reordering sibling nodes via native Drag-and-Drop into top (before) and bottom (after) zones."""
    create_root_node(page, "FirstRoot", data_type="Text")
    create_root_node(page, "SecondRoot", data_type="Text")
    create_root_node(page, "ThirdRoot", data_type="Text")

    first_card = page.locator(".tree-node-content:has(.node-title:has-text('FirstRoot'))").first
    second_card = page.locator(".tree-node-content:has(.node-title:has-text('SecondRoot'))").first
    third_card = page.locator(".tree-node-content:has(.node-title:has-text('ThirdRoot'))").first

    # Drag SecondRoot before FirstRoot (targeting top 10% of first_card)
    second_card.drag_to(first_card, target_position={"x": 50, "y": 4})
    expect(page.locator(".tree-node .node-title").first).to_have_text("SecondRoot")

    # Drag FirstRoot after ThirdRoot (targeting bottom 90% of third_card)
    first_card.drag_to(third_card, target_position={"x": 50, "y": 36})
    expect(page.locator(".tree-node .node-title").last).to_have_text("FirstRoot")


@pytest.mark.e2e
def test_cycle_detection_prohibits_parent_into_child(page: Page):
    """Verifies that dragging a parent node into its own descendant is rejected with a warning toast."""
    create_root_node(page, "MainParent", data_type="Text")
    add_child_node(page, "MainParent", "SubChild", data_type="Text")

    parent_card = page.locator(".tree-node-content:has(.node-title:has-text('MainParent'))").first
    child_card = page.locator(".tree-node-content:has(.node-title:has-text('SubChild'))").first

    expect(parent_card).to_be_visible()
    expect(child_card).to_be_visible()

    # Attempt illegal native drag: drop parent into its child center
    parent_card.drag_to(child_card, target_position={"x": 50, "y": 20})

    # Verify warning toast appears and parent-child tree structure is preserved
    expect(page.locator(".toast.toast-warning")).to_be_visible()
    expect(page.locator(".tree-node:has(.node-title:has-text('MainParent'))")).to_be_visible()
