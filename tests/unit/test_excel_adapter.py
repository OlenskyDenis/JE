"""Unit tests for ExcelHierarchyAdapter Row 1 header reading, sheet management, and horizontal re-export."""

import tempfile
import os
import openpyxl
from src.hierarchy_lib.adapters.excel_adapter import ExcelHierarchyAdapter


def test_get_sheet_names_and_read_row1_headers():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Sales"
        ws1.cell(row=1, column=1, value=" Region ")
        ws1.cell(row=1, column=2, value="Revenue")
        ws1.cell(row=1, column=3, value=" Region ")  # duplicate
        ws1.cell(row=2, column=1, value="Ignore Row 2 Data")

        ws2 = wb.create_sheet(title="Inventory")
        ws2.cell(row=1, column=1, value="Stock ID")
        ws2.cell(row=1, column=2, value=" Quantity ")

        wb.save(tmp_path)
        wb.close()

        # Test sheet listing
        sheet_names = ExcelHierarchyAdapter.get_sheet_names(tmp_path)
        assert sheet_names == ["Sales", "Inventory"]

        # Test Row 1 header extraction (deduplicated, trimmed, sorted)
        sales_headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "Sales")
        assert sales_headers == ["Region", "Revenue"]

        inv_headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "Inventory")
        assert inv_headers == ["Quantity", "Stock ID"]

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_horizontal_row1_leaf_paths():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create base workbook
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "DataSheet"
        ws1.cell(row=1, column=1, value="OldHeader1")
        ws1.cell(row=2, column=1, value="PreservedRow2Data")
        ws2 = wb.create_sheet(title="UneditedSheet")
        ws2.cell(row=1, column=1, value="Unchanged")
        wb.save(tmp_path)
        wb.close()

        # Export reconstructed horizontal leaf paths into Row 1 of DataSheet
        new_paths = ["Root\\Folder1\\ItemA", "Root\\Folder2\\ItemB"]
        cols_written = ExcelHierarchyAdapter.export_horizontal_row1_leaf_paths(
            file_path_or_stream=tmp_path,
            sheet_name="DataSheet",
            leaf_paths=new_paths,
            output_path=tmp_path
        )

        assert cols_written == 2

        # Verify output file
        wb_out = openpyxl.load_workbook(tmp_path)
        assert "DataSheet" in wb_out.sheetnames
        assert "UneditedSheet" in wb_out.sheetnames

        ws_data = wb_out["DataSheet"]
        assert ws_data.cell(row=1, column=1).value == "Root\\Folder1\\ItemA"
        assert ws_data.cell(row=1, column=2).value == "Root\\Folder2\\ItemB"
        # Verify Row 2 preserved
        assert ws_data.cell(row=2, column=1).value == "PreservedRow2Data"
        # Verify UneditedSheet preserved
        assert wb_out["UneditedSheet"].cell(row=1, column=1).value == "Unchanged"
        wb_out.close()

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
