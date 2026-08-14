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
        assert headers == ["Department", "ID", "Name"]
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
