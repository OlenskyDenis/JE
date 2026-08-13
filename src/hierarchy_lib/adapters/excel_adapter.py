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
    def read_row1_headers(file_path_or_stream: Union[str, BinaryIO], sheet_name: str) -> List[str]:
        """Reads Row 1 cells exclusively from the specified sheet, returns clean, deduplicated, sorted headers."""
        wb = openpyxl.load_workbook(file_path_or_stream, data_only=True)
        if sheet_name not in wb.sheetnames:
            wb.close()
            return []

        sheet = wb[sheet_name]
        raw_headers = []
        # Read exclusively Row 1 across max columns
        max_col = sheet.max_column or 1
        for col_idx in range(1, max_col + 1):
            val = sheet.cell(row=1, column=col_idx).value
            if val is not None:
                raw_headers.append(val)

        wb.close()
        return HeaderService.process_headers(raw_headers)

    @staticmethod
    def export_horizontal_row1_leaf_paths(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        leaf_paths: List[str],
        output_path: str
    ) -> int:
        """
        Writes leaf_paths sequentially into Row 1 across columns (A1, B1, C1...) for target sheet_name.
        Preserves lower rows (Row 2+) and unedited sheets in the workbook.
        Returns the number of columns written.
        """
        if isinstance(file_path_or_stream, str) and os.path.exists(file_path_or_stream):
            wb = openpyxl.load_workbook(file_path_or_stream)
        else:
            wb = openpyxl.Workbook()

        if sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
        else:
            sheet = wb.create_sheet(title=sheet_name)

        # Write leaf path strings into Row 1 horizontally across columns
        for col_idx, path_str in enumerate(leaf_paths, start=1):
            sheet.cell(row=1, column=col_idx, value=path_str)

        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        wb.save(output_path)
        wb.close()
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
