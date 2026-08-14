"""ExcelHierarchyAdapter using openpyxl for self-contained Excel processing."""

import os
from typing import Union, BinaryIO, List
import openpyxl
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.header_service import HeaderService


class ExcelHierarchyAdapter:
    """Adapter for importing and exporting Composite hierarchy trees to/from Excel (.xlsx) files."""

    @staticmethod
    def get_sheet_names(file_path_or_stream: Union[str, BinaryIO]) -> List[str]:
        """Returns the list of worksheet names available in the workbook."""
        wb = openpyxl.load_workbook(file_path_or_stream, read_only=True)
        names = list(wb.sheetnames)
        wb.close()
        return names

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
        wb = openpyxl.load_workbook(file_path_or_stream, read_only=True, data_only=True)
        try:
            if sheet_name not in wb.sheetnames:
                return []

            sheet = wb[sheet_name]
            raw_headers = []
            consecutive_empty = 0

            # Stream strictly Row 1
            row_generator = sheet.iter_rows(max_row=1, values_only=True)
            first_row = next(row_generator, None)

            if first_row is not None:
                for val in first_row:
                    if val is not None and str(val).strip() != "":
                        consecutive_empty = 0
                        raw_headers.append(val)
                    else:
                        consecutive_empty += 1
                        if consecutive_empty >= max_empty_consecutive:
                            break

            return HeaderService.process_headers(raw_headers)
        finally:
            wb.close()

    @staticmethod
    def export_multi_sheet_template(
        file_path_or_stream: Union[str, BinaryIO, None],
        sheet_leaf_paths_map: Dict[str, List[str]],
        output_path: str
    ) -> int:
        """
        Constructs a fresh openpyxl.Workbook() from scratch containing all original sheets with Row 1 headers only.
        For each sheet in sheet_leaf_paths_map: writes custom leaf_paths across Row 1 columns (A1, B1, C1...).
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
                # Target reorganized sheet: write leaf_paths into Row 1
                paths = sheet_leaf_paths_map[sname]
                for col_idx, path_str in enumerate(paths, start=1):
                    ws.cell(row=1, column=col_idx, value=path_str)
                total_cols += len(paths)
            elif has_source:
                # Other sheets: stream original Row 1 headers without reading data rows
                other_headers = ExcelHierarchyAdapter.read_row1_headers(file_path_or_stream, sname)
                for col_idx, h_str in enumerate(other_headers, start=1):
                    ws.cell(row=1, column=col_idx, value=h_str)
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
