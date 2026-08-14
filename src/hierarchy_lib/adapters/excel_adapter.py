"""ExcelHierarchyAdapter using openpyxl for self-contained Excel processing."""

import os
from typing import Union, BinaryIO, List, Dict, Any, Tuple, Optional
from collections import Counter
import openpyxl
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.header_service import HeaderService


class ExcelHierarchyAdapter:
    """Adapter for importing and exporting Composite hierarchy trees to/from Excel (.xlsx) files."""

    EXCEL_TYPE_FORMAT_MAP = {
        "Text": "@",
        "Integer": "0",
        "Decimal": "0.00",
        "Currency": '"$"#,##0.00',
        "Percentage": "0.00%",
        "Date": "yyyy-mm-dd",
        "Time": "hh:mm:ss",
        "DateTime": "yyyy-mm-dd hh:mm:ss",
        "Boolean": "General",
    }

    @staticmethod
    def get_sheet_names(file_path_or_stream: Union[str, BinaryIO]) -> List[str]:
        """Returns the list of worksheet names available in the workbook."""
        wb = openpyxl.load_workbook(file_path_or_stream, read_only=True)
        names = list(wb.sheetnames)
        wb.close()
        return names

    @staticmethod
    def _map_format_to_data_type(
        number_format: Optional[str],
        data_type_flag: Optional[str] = None,
        header_name: Optional[str] = None
    ) -> str:
        """Maps Excel number format string and cell data_type flag to one of the 9 standard Excel types."""
        if data_type_flag == "b":
            return "Boolean"

        num_fmt = (number_format or "").strip().lower()
        if not num_fmt or num_fmt in ("@", "general"):
            if data_type_flag == "d":
                return "Date"
            return "Text"

        has_time = any(t in num_fmt for t in ("h", "s", "am/pm"))
        has_date = any(d in num_fmt for d in ("y", "d", "mmm", "m/d")) or ("m" in num_fmt and not has_time and "/" in num_fmt)

        if "%" in num_fmt:
            return "Percentage"

        if any(curr in num_fmt for curr in ("$", "€", "£", "грн", "₽", "¥", "руб", "¤", "[$")):
            return "Currency"

        if has_date and has_time:
            return "DateTime"
        if has_time and not has_date:
            return "Time"
        if has_date:
            return "Date"

        if "0.00" in num_fmt or "#.00" in num_fmt or "0.0" in num_fmt:
            return "Decimal"

        if num_fmt in ("0", "#,##0", "0_"):
            return "Integer"

        return "Text"

    @staticmethod
    def read_row1_headers_and_types(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        max_empty_consecutive: int = 10
    ) -> List[Tuple[str, str]]:
        """
        Reads Row 1 cells strictly in streaming mode (max_row=1).
        For each valid header, extracts the header name and determines the configured
        Excel column data type based on cell.number_format, column_dimensions.number_format,
        and cell.data_type.
        Stops scanning if max_empty_consecutive empty/None cells are encountered.
        Returns a list of tuples: [(header_name, data_type), ...]
        """
        wb = openpyxl.load_workbook(file_path_or_stream, data_only=False)
        try:
            if sheet_name not in wb.sheetnames:
                return []

            sheet = wb[sheet_name]
            raw_items = []
            consecutive_empty = 0
            max_col = sheet.max_column or 100

            for col_idx in range(1, max_col + 1):
                cell = sheet.cell(row=1, column=col_idx)
                val = cell.value
                if val is not None and str(val).strip() != "":
                    consecutive_empty = 0
                    col_letter = openpyxl.utils.get_column_letter(col_idx)
                    col_dim_fmt = ""
                    if col_letter in sheet.column_dimensions:
                        col_dim_fmt = sheet.column_dimensions[col_letter].number_format or ""

                    num_fmt = cell.number_format or col_dim_fmt or ""
                    detected_type = ExcelHierarchyAdapter._map_format_to_data_type(
                        number_format=num_fmt,
                        data_type_flag=cell.data_type,
                        header_name=str(val).strip()
                    )
                    raw_items.append((str(val).strip(), detected_type))
                else:
                    consecutive_empty += 1
                    if consecutive_empty >= max_empty_consecutive:
                        break

            # Deduplicate preserving original sequence
            seen = set()
            result = []
            for name, dtype in raw_items:
                if name not in seen:
                    seen.add(name)
                    result.append((name, dtype))

            return result
        finally:
            wb.close()

    @staticmethod
    def infer_column_types(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        max_rows: int = 1
    ) -> Dict[str, str]:
        """Infers standard Excel column data types directly from Row 1 column formats."""
        pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(file_path_or_stream, sheet_name)
        return dict(pairs)

    @staticmethod
    def read_row1_headers(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        max_empty_consecutive: int = 10
    ) -> List[str]:
        """
        Reads Row 1 cells exclusively from the specified sheet in read_only streaming mode.
        Ignores rows 2+ completely, and stops scanning if max_empty_consecutive empty/None
        cells are encountered in Row 1.
        Returns clean, deduplicated, sorted headers.
        """
        pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(
            file_path_or_stream, sheet_name, max_empty_consecutive=max_empty_consecutive
        )
        return HeaderService.process_headers([name for name, _ in pairs])

    @staticmethod
    def export_multi_sheet_template(
        file_path_or_stream: Union[str, BinaryIO, None],
        sheet_leaf_paths_map: Dict[str, Any],
        output_path: str
    ) -> int:
        """
        Constructs a fresh openpyxl.Workbook() from scratch containing all original sheets with Row 1 headers only.
        For each sheet in sheet_leaf_paths_map: writes custom leaf_paths across Row 1 columns (A1, B1, C1...) and applies number_format.
        For all other sheets: streams original Row 1 headers without reading data rows.
        Guarantees zero data rows in Row 2+ across all sheets with minimal memory/CPU overhead.
        Returns total columns written across all sheets.
        """
        new_wb = openpyxl.Workbook()

        has_source = isinstance(file_path_or_stream, str) and os.path.exists(file_path_or_stream)

        if has_source:
            sheet_names = ExcelHierarchyAdapter.get_sheet_names(file_path_or_stream)
            for sname in sheet_leaf_paths_map.keys():
                if sname and sname not in sheet_names:
                    sheet_names.append(sname)
        else:
            sheet_names = list(sheet_leaf_paths_map.keys()) if sheet_leaf_paths_map else ["Sheet1"]

        total_cols = 0
        for idx, sname in enumerate(sheet_names):
            if idx == 0:
                ws = new_wb.active
                ws.title = sname
            else:
                ws = new_wb.create_sheet(title=sname)

            if sname in sheet_leaf_paths_map:
                # Target reorganized sheet: write leaf_paths and format types into Row 1
                items = sheet_leaf_paths_map[sname]
                for col_idx, item in enumerate(items, start=1):
                    path_str = ""
                    data_type = "Text"

                    if isinstance(item, str):
                        path_str = item
                    elif isinstance(item, dict):
                        path_str = item.get("path") or item.get("name") or ""
                        data_type = item.get("type") or item.get("data_type") or "Text"
                    elif isinstance(item, (tuple, list)):
                        path_str = item[0] if len(item) > 0 else ""
                        data_type = item[1] if len(item) > 1 else "Text"

                    cell = ws.cell(row=1, column=col_idx, value=path_str)
                    fmt = ExcelHierarchyAdapter.EXCEL_TYPE_FORMAT_MAP.get(data_type, "@")
                    cell.number_format = fmt

                total_cols += len(items)
            elif has_source:
                # Other sheets: stream original Row 1 headers without reading data rows
                other_headers = ExcelHierarchyAdapter.read_row1_headers(file_path_or_stream, sname)
                for col_idx, h_str in enumerate(other_headers, start=1):
                    cell = ws.cell(row=1, column=col_idx, value=h_str)
                    cell.number_format = "@"
                total_cols += len(other_headers)

        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        new_wb.save(output_path)
        new_wb.close()
        return total_cols


    @staticmethod
    def export_horizontal_row1_leaf_paths(
        file_path_or_stream: Union[str, BinaryIO, None],
        sheet_name: str,
        leaf_paths: List[str],
        output_path: str
    ) -> int:
        """Backwards-compatible wrapper calling export_multi_sheet_template."""
        ExcelHierarchyAdapter.export_multi_sheet_template(
            file_path_or_stream=file_path_or_stream,
            sheet_leaf_paths_map={sheet_name: leaf_paths},
            output_path=output_path
        )
        return len(leaf_paths)

    @staticmethod
    def import_from_file(file_path_or_stream: Union[str, BinaryIO]) -> WorkspaceForest:
        """
        Parses an Excel (.xlsx) file into a WorkspaceForest.
        Reads Row 1 / Cell A1 of each sheet in the workbook as a backslash-separated path string.
        """
        forest = WorkspaceForest()
        wb = openpyxl.load_workbook(file_path_or_stream, data_only=True)

        for sheet in wb.worksheets:
            cell_value = sheet.cell(row=1, column=1).value
            if not cell_value or not str(cell_value).strip():
                continue

            path_str = str(cell_value).strip()
            segments = [seg.strip() for seg in path_str.split("\\") if seg.strip()]
            if not segments:
                continue

            # Segment 0 is root
            root_name = segments[0]
            current_container = None
            for root in forest.root_nodes:
                if root.name == root_name:
                    current_container = root
                    break

            if not current_container:
                current_container = CompositeNode(root_name)
                forest.add_root(current_container)

            # Process subsequent path segments
            for idx in range(1, len(segments)):
                seg_name = segments[idx]
                is_last = (idx == len(segments) - 1)

                if is_last:
                    existing_child = None
                    for child in current_container.children:
                        if child.name == seg_name:
                            existing_child = child
                            break

                    if not existing_child:
                        leaf = LeafNode(seg_name)
                        current_container.add_child(leaf)
                else:
                    existing_container = None
                    for child in current_container.children:
                        if child.is_container and child.name == seg_name and isinstance(child, CompositeNode):
                            existing_container = child
                            break

                    if not existing_container:
                        new_container = CompositeNode(seg_name)
                        current_container.add_child(new_container)
                        current_container = new_container
                    else:
                        current_container = existing_container

        wb.close()
        return forest

    @staticmethod
    def export_to_file(forest: WorkspaceForest, output_path: str) -> int:
        """
        Exports all leaf paths from the WorkspaceForest into an Excel (.xlsx) workbook.
        Each leaf path is assigned a sheet, writing each path segment down Column A.
        Returns the total number of paths exported.
        """
        wb = openpyxl.Workbook()
        default_sheet = wb.active
        wb.remove(default_sheet)

        paths = forest.get_all_leaf_paths()
        if not paths:
            sheet = wb.create_sheet(title="Hierarchy")
            sheet.cell(row=1, column=1, value="")
        else:
            for idx, path_str in enumerate(paths, start=1):
                segments = [seg for seg in path_str.split("\\") if seg]
                sheet_title = f"Path_{idx}"
                sheet = wb.create_sheet(title=sheet_title)

                for row_idx, seg in enumerate(segments, start=1):
                    sheet.cell(row=row_idx, column=1, value=seg)

        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        wb.save(output_path)
        wb.close()
        return len(paths)
