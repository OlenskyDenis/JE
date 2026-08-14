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

        # Test Row 1 header extraction (deduplicated, trimmed, original column sequence)
        sales_headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "Sales")
        assert sales_headers == ["Region", "Revenue"]

        inv_headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "Inventory")
        assert inv_headers == ["Stock ID", "Quantity"]

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_horizontal_row1_leaf_paths():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create base workbook with multiple sheets and data rows in Row 2+
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "DataSheet"
        ws1.cell(row=1, column=1, value="OldHeader1")
        ws1.cell(row=2, column=1, value="ShouldBeStrippedData")
        ws1.cell(row=3, column=1, value="ShouldBeStrippedDataRow3")
        ws2 = wb.create_sheet(title="UneditedSheet")
        ws2.cell(row=1, column=1, value="UnchangedHeader")
        ws2.cell(row=2, column=1, value="ShouldBeStrippedDataInSheet2")
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

        # Verify output file is a clean template with all sheets preserved and ZERO data rows
        wb_out = openpyxl.load_workbook(tmp_path)
        assert wb_out.sheetnames == ["DataSheet", "UneditedSheet"]

        ws_data = wb_out["DataSheet"]
        assert ws_data.cell(row=1, column=1).value == "Root\\Folder1\\ItemA"
        assert ws_data.cell(row=1, column=2).value == "Root\\Folder2\\ItemB"
        # Verify Row 2+ data is stripped (max_row == 1, row 2 is None)
        assert ws_data.max_row == 1
        assert ws_data.cell(row=2, column=1).value is None

        # Verify UneditedSheet preserved with its original Row 1 header and zero data rows
        ws_unedited = wb_out["UneditedSheet"]
        assert ws_unedited.cell(row=1, column=1).value == "UnchangedHeader"
        assert ws_unedited.max_row == 1
        assert ws_unedited.cell(row=2, column=1).value is None
        wb_out.close()

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_multi_sheet_template():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_src, \
         tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_out:
        src_path = tmp_src.name
        out_path = tmp_out.name

    try:
        # Create source workbook with 3 sheets and data rows
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Sales"
        ws1.cell(row=1, column=1, value="OldSales1")
        ws1.cell(row=2, column=1, value="SalesData")

        ws2 = wb.create_sheet(title="Inventory")
        ws2.cell(row=1, column=1, value="OldInv1")
        ws2.cell(row=2, column=1, value="InvData")

        ws3 = wb.create_sheet(title="Reference")
        ws3.cell(row=1, column=1, value="RefHeader1")
        ws3.cell(row=2, column=1, value="RefData")
        wb.save(src_path)
        wb.close()

        # Simultaneously export modified leaf paths for Sales and Inventory, leaving Reference unmodified
        sheet_map = {
            "Sales": ["Sales\\North\\A", "Sales\\South\\B"],
            "Inventory": ["Inv\\Warehouse\\Bin1", "Inv\\Warehouse\\Bin2", "Inv\\Warehouse\\Bin3"]
        }

        total_cols = ExcelHierarchyAdapter.export_multi_sheet_template(
            file_path_or_stream=src_path,
            sheet_leaf_paths_map=sheet_map,
            output_path=out_path
        )

        assert total_cols == 2 + 3 + 1  # Sales(2) + Inventory(3) + Reference(1 streamed)

        wb_out = openpyxl.load_workbook(out_path)
        assert wb_out.sheetnames == ["Sales", "Inventory", "Reference"]

        # Check Sales
        ws_sales = wb_out["Sales"]
        assert ws_sales.cell(row=1, column=1).value == "Sales\\North\\A"
        assert ws_sales.cell(row=1, column=2).value == "Sales\\South\\B"
        assert ws_sales.max_row == 1

        # Check Inventory
        ws_inv = wb_out["Inventory"]
        assert ws_inv.cell(row=1, column=1).value == "Inv\\Warehouse\\Bin1"
        assert ws_inv.cell(row=1, column=2).value == "Inv\\Warehouse\\Bin2"
        assert ws_inv.cell(row=1, column=3).value == "Inv\\Warehouse\\Bin3"
        assert ws_inv.max_row == 1

        # Check Reference (streamed original header, zero data rows)
        ws_ref = wb_out["Reference"]
        assert ws_ref.cell(row=1, column=1).value == "RefHeader1"
        assert ws_ref.max_row == 1

        wb_out.close()
    finally:
        if os.path.exists(src_path):
            os.remove(src_path)
        if os.path.exists(out_path):
            os.remove(out_path)


def test_round_trip_parse_and_export():
    from src.hierarchy_lib.services.path_parser import PathParserService
    from src.hierarchy_lib.services.path_generator import PathGenerator

    initial_headers = [r"Company\HR\Employees", r"Company\HR\Salaries", r"Company\Finance\Invoices"]
    forest = PathParserService.parse_header_paths(initial_headers)
    leaf_paths = PathGenerator.calculate_all_paths(forest)

    assert leaf_paths == initial_headers


def test_read_row1_headers_read_only_streaming_large_sheet():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "LargeSheet"
        # Row 1 headers
        ws.cell(row=1, column=1, value="ID")
        ws.cell(row=1, column=2, value="Name")
        ws.cell(row=1, column=3, value="Department")

        # Add 1,000 data rows to simulate large sheet
        for r in range(2, 1002):
            ws.cell(row=r, column=1, value=r)
            ws.cell(row=r, column=2, value=f"User_{r}")
            ws.cell(row=r, column=3, value="Engineering")

        wb.save(tmp_path)
        wb.close()

        headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "LargeSheet")
        assert headers == ["ID", "Name", "Department"]
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_read_row1_headers_consecutive_empty_cutoff():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "CutoffSheet"
        ws.cell(row=1, column=1, value="ColA")
        ws.cell(row=1, column=2, value="ColB")
        # Columns 3 to 12 are left empty (10 consecutive empty cells)
        # Column 13 has a distant header that should be ignored
        ws.cell(row=1, column=13, value="DistantCol")

        wb.save(tmp_path)
        wb.close()

        headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "CutoffSheet")
        assert "DistantCol" not in headers
        assert headers == ["ColA", "ColB"]
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_read_row1_headers_small_gap_allowed():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "GapSheet"
        ws.cell(row=1, column=1, value="ColA")
        # Columns 2, 3, 4 empty (3 consecutive empty cells < 10)
        ws.cell(row=1, column=5, value="ColB")

        wb.save(tmp_path)
        wb.close()

        headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "GapSheet")
        assert headers == ["ColA", "ColB"]
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_read_row1_headers_whitespace_counts_as_empty():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "WhitespaceSheet"
        ws.cell(row=1, column=1, value="Header1")
        # Columns 2..11 are whitespace only
        for c in range(2, 12):
            ws.cell(row=1, column=c, value="   ")
        ws.cell(row=1, column=12, value="Header2")

        wb.save(tmp_path)
        wb.close()

        headers = ExcelHierarchyAdapter.read_row1_headers(tmp_path, "WhitespaceSheet")
        assert "Header2" not in headers
        assert headers == ["Header1"]
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
