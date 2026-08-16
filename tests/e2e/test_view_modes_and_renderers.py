"""E2E browser tests for View Mode Switcher, Excel Blocks Matrix, and Unique Levels Rendering (Features 027, 028, 030)."""

import pytest
from playwright.sync_api import Page, expect
from tests.e2e.conftest import create_root_node, add_child_node


@pytest.mark.e2e
def test_view_mode_switching_between_tree_matrix_and_unique_levels(page: Page):
    """Verifies seamless switching across Tree View, Excel Blocks View, and Unique Levels View."""
    # 1. Create a structured hierarchy in tree view
    create_root_node(page, "Company", data_type="Text")
    add_child_node(page, "Company", "Finance", data_type="Text")
    add_child_node(page, "Finance", "Budget2026", data_type="Currency")

    expect(page.locator("#treeView")).to_be_visible()
    expect(page.locator("#excelBlockView")).to_have_class("excel-block-view hidden")
    expect(page.locator("#uniqueLevelView")).to_have_class("unique-level-view hidden")

    # 2. Switch to Excel Blocks View (Matrix)
    page.click("#btnViewMatrix")
    expect(page.locator("#btnViewMatrix")).to_have_class("view-mode-btn active")
    expect(page.locator("#treeView")).to_have_class("tree-root-container hidden")
    expect(page.locator("#excelBlockView")).not_to_have_class("hidden")
    expect(page.locator(".excel-matrix-table")).to_be_visible()
    expect(page.locator(".matrix-cell-title:has-text('Company')")).to_be_visible()
    expect(page.locator(".matrix-cell-title:has-text('Budget2026')")).to_be_visible()

    # 3. Switch to Unique by Levels View
    page.click("#btnViewUniqueLevels")
    expect(page.locator("#btnViewUniqueLevels")).to_have_class("view-mode-btn active")
    expect(page.locator("#excelBlockView")).to_have_class("excel-block-view hidden")
    expect(page.locator("#uniqueLevelView")).not_to_have_class("hidden")
    expect(page.locator(".unique-levels-wrapper")).to_be_visible()
    expect(page.locator(".level-row-container")).to_have_count(3)
    expect(page.locator(".chip-title:has-text('Company')")).to_be_visible()
    expect(page.locator(".chip-title:has-text('Budget2026')")).to_be_visible()

    # 4. Switch back to Tree View
    page.click("#btnViewTree")
    expect(page.locator("#btnViewTree")).to_have_class("view-mode-btn active")
    expect(page.locator("#treeView")).not_to_have_class("hidden")
    expect(page.locator(".tree-node .node-title:has-text('Company')")).to_be_visible()


@pytest.mark.e2e
def test_excel_block_matrix_rendering_and_coordinates(page: Page):
    """Verifies that Excel Block View renders spreadsheet coordinates, leaf tags, and merged spans."""
    create_root_node(page, "Sales", data_type="Text")
    add_child_node(page, "Sales", "Q1", data_type="Currency")
    add_child_node(page, "Sales", "Q2", data_type="Currency")

    page.click("#btnViewMatrix")
    expect(page.locator(".excel-matrix-table")).to_be_visible()

    # Coordinates row should have columns A and B
    expect(page.locator(".matrix-coord-header:has-text('A')")).to_be_visible()
    expect(page.locator(".matrix-coord-header:has-text('B')")).to_be_visible()

    # Parent 'Sales' spans 2 columns
    sales_cell = page.locator(".matrix-cell-folder:has-text('Sales')")
    expect(sales_cell).to_have_attribute("colspan", "2")

    # Leaf items show currency type badge
    expect(page.locator(".matrix-cell-leaf:has-text('Q1') .matrix-cell-type-tag")).to_contain_text("Валюта")
    expect(page.locator(".matrix-cell-leaf:has-text('Q2') .matrix-cell-type-tag")).to_contain_text("Валюта")


@pytest.mark.e2e
def test_unique_level_view_leaf_and_branch_partitioning(page: Page):
    """Verifies unique levels partitions leaves first and branches second with visual separator."""
    create_root_node(page, "HR", data_type="Text")
    add_child_node(page, "HR", "Recruitment", data_type="Text")
    add_child_node(page, "HR", "Payroll", data_type="Currency")  # Leaf at Tier 1
    add_child_node(page, "Recruitment", "Interns", data_type="Integer")  # Recruitment is a branch at Tier 1

    page.click("#btnViewUniqueLevels")
    expect(page.locator("#uniqueLevelView")).not_to_have_class("hidden")

    # Tier 1 row (containing Payroll as leaf and Recruitment as branch)
    tier1_row = page.locator(".level-row-container.level-tier-1")
    expect(tier1_row).to_be_visible()

    # Check leaves subgroup and branches subgroup
    expect(tier1_row.locator(".level-group-leaves .chip-title:has-text('Payroll')")).to_be_visible()
    expect(tier1_row.locator(".level-group-branches .chip-title:has-text('Recruitment')")).to_be_visible()
    expect(tier1_row.locator(".level-group-separator")).to_be_visible()
