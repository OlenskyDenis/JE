"""Integration & contract tests for Eel RPC bridge endpoints."""

import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
import openpyxl
import src.app.eel_bridge as bridge


def setup_function():
    """Reset global workspace forest and file session before each test."""
    bridge.forest.root_nodes.clear()
    bridge.current_file_path = None


def test_eel_add_and_get_workspace_tree():
    res1 = bridge.add_node(None, "RootA", is_container=True)
    assert res1["success"] is True
    root_id = res1["node"]["id"]

    res2 = bridge.add_node(root_id, "ChildA", is_container=False)
    assert res2["success"] is True

    tree = bridge.get_workspace_tree()
    assert tree["success"] is True
    assert len(tree["roots"]) == 1
    assert tree["roots"][0]["name"] == "RootA"
    assert tree["roots"][0]["children"][0]["name"] == "ChildA"
    assert tree["roots"][0]["children"][0]["absolute_path"] == "RootA\\ChildA"


def test_eel_move_node_cycle_rejection():
    res1 = bridge.add_node(None, "Parent", is_container=True)
    p_id = res1["node"]["id"]

    res2 = bridge.add_node(p_id, "Child", is_container=True)
    c_id = res2["node"]["id"]

    # Attempt to move Parent into Child -> Should reject cycle
    move_res = bridge.move_node(p_id, c_id, "NEST_CHILD")
    assert move_res["success"] is False
    assert "descendant" in move_res["rejection_reason"]


def test_eel_import_export_excel():
    # Setup tree
    res1 = bridge.add_node(None, "Root", is_container=True)
    r_id = res1["node"]["id"]
    bridge.add_node(r_id, "Leaf1", is_container=False)

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Export
        exp_res = bridge.export_excel(tmp_path)
        assert exp_res["success"] is True
        assert exp_res["exported_paths"] == 1

        # Import into fresh state
        bridge.forest.root_nodes.clear()
        imp_res = bridge.import_excel(tmp_path)
        assert imp_res["success"] is True
        assert len(imp_res["roots"]) == 1
        assert imp_res["roots"][0]["name"] == "Root"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_eel_sidebar_reorganizer_rpc_flow():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create Excel file with 2 sheets
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "SheetA"
        ws1.cell(row=1, column=1, value=" Header 2 ")
        ws1.cell(row=1, column=2, value="Header 1")

        ws2 = wb.create_sheet(title="SheetB")
        ws2.cell(row=1, column=1, value="Category")
        wb.save(tmp_path)
        wb.close()

        # 1. Test import_excel_file with hierarchical headers
        res_import = bridge.import_excel_file(tmp_path)
        assert res_import["success"] is True
        assert res_import["sheets"] == ["SheetA", "SheetB"]
        assert res_import["active_sheet"] == "SheetA"
        assert res_import["headers"] == ["Header 1", "Header 2"]  # sorted
        assert "roots" in res_import
        assert len(res_import["roots"]) == 2

        # 2. Test switch_active_sheet with roots regeneration
        res_switch = bridge.switch_active_sheet("SheetB")
        assert res_switch["success"] is True
        assert res_switch["sheet_name"] == "SheetB"
        assert res_switch["headers"] == ["Category"]
        assert "roots" in res_switch
        assert len(res_switch["roots"]) == 1
        assert res_switch["roots"][0]["name"] == "Category"

        # 3. Test export_reorganized_row1
        leaf_paths = ["Root\\Folder\\ItemA", "Root\\Folder\\ItemB"]
        res_export = bridge.export_reorganized_row1("SheetA", leaf_paths, tmp_path)
        assert res_export["success"] is True
        assert res_export["column_count"] == 2

        # Verify exported file
        wb_check = openpyxl.load_workbook(tmp_path)
        assert wb_check["SheetA"].cell(row=1, column=1).value == "Root\\Folder\\ItemA"
        assert wb_check["SheetA"].cell(row=1, column=2).value == "Root\\Folder\\ItemB"
        wb_check.close()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@patch("src.hierarchy_lib.services.dialog_service.filedialog.askopenfilename")
@patch("src.hierarchy_lib.services.dialog_service.filedialog.asksaveasfilename")
@patch("src.hierarchy_lib.services.dialog_service.tk.Tk")
def test_eel_file_dialog_rpc_endpoints(mock_tk, mock_asksave, mock_askopen):
    mock_askopen.return_value = "E:/Data/test_import.xlsx"
    mock_asksave.return_value = "E:/Data/test_export.xlsx"

    open_res = bridge.open_file_dialog()
    assert open_res["success"] is True
    assert open_res["cancelled"] is False
    assert open_res["file_path"] == "E:/Data/test_import.xlsx"

    save_res = bridge.save_file_dialog("default.xlsx")
    assert save_res["success"] is True
    assert save_res["cancelled"] is False
    assert save_res["file_path"] == "E:/Data/test_export.xlsx"


def test_eel_add_node_with_zone_positioning():
    # 1. Create root node A and child node B
    res_root = bridge.add_node(None, "RootA", is_container=True)
    root_id = res_root["node"]["id"]

    res_child_b = bridge.add_node(root_id, "NodeB", is_container=True)
    b_id = res_child_b["node"]["id"]

    # 2. Add header BEFORE NodeB
    res_before = bridge.add_node(name="HeaderBefore", is_container=False, target_id=b_id, zone="BEFORE_SIBLING")
    assert res_before["success"] is True

    # 3. Add header AFTER NodeB
    res_after = bridge.add_node(name="HeaderAfter", is_container=False, target_id=b_id, zone="AFTER_SIBLING")
    assert res_after["success"] is True

    # 4. Add header NEST_CHILD inside NodeB
    res_inside = bridge.add_node(name="HeaderInside", is_container=False, target_id=b_id, zone="NEST_CHILD")
    assert res_inside["success"] is True

    tree = bridge.get_workspace_tree()
    root_node = tree["roots"][0]
    children_names = [c["name"] for c in root_node["children"]]
    assert children_names == ["HeaderBefore", "NodeB", "HeaderAfter"]

    node_b = root_node["children"][1]
    assert node_b["children"][0]["name"] == "HeaderInside"


def test_eel_hierarchical_excel_import_and_switch():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Sales"
        ws1.cell(row=1, column=1, value=r"Company\Sales\Orders")
        ws1.cell(row=1, column=2, value=r"Company\Sales\Customers")
        ws1.cell(row=1, column=3, value=r"Company\HR\Employees")

        ws2 = wb.create_sheet(title="Warehouse")
        ws2.cell(row=1, column=1, value=r"Inventory\Stock\Items")
        wb.save(tmp_path)
        wb.close()

        # Import file: should auto-generate hierarchy for Sales
        res1 = bridge.import_excel_file(tmp_path)
        assert res1["success"] is True
        roots1 = res1["roots"]
        assert len(roots1) == 1
        assert roots1[0]["name"] == "Company"
        folder_names = [c["name"] for c in roots1[0]["children"]]
        assert "Sales" in folder_names
        assert "HR" in folder_names

        # Switch to Warehouse: should regenerate hierarchy for Warehouse
        res2 = bridge.switch_active_sheet("Warehouse")
        assert res2["success"] is True
        roots2 = res2["roots"]
        assert len(roots2) == 1
        assert roots2[0]["name"] == "Inventory"
        assert roots2[0]["children"][0]["name"] == "Stock"
        assert roots2[0]["children"][0]["children"][0]["name"] == "Items"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

