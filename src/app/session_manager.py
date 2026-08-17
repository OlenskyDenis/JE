"""SessionManager for Excel workbook multi-sheet hierarchies, session state, and template synchronization."""

import os
from typing import Any, Dict, List, Optional, Tuple

from src.hierarchy_lib.adapters.excel_adapter import ExcelHierarchyAdapter
from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.path_parser import PathParserService
from src.hierarchy_lib.services.settings_service import SettingsService


class SessionManager:
    """Manages multi-sheet session forests, active sheet tracking, and template syncing."""

    def __init__(self):
        self.forest = WorkspaceForest()
        self.sheet_forests: Dict[str, WorkspaceForest] = {}
        self.current_active_sheet: Optional[str] = None
        self.current_file_path: Optional[str] = None
        self.current_template_path: Optional[str] = None

    def reset_workspace(self) -> None:
        """Resets the session state and active forest to clean empty defaults."""
        self.forest = WorkspaceForest()
        self.sheet_forests = {}
        self.current_active_sheet = None
        self.current_file_path = None
        self.current_template_path = None

    @staticmethod
    def get_forest_leaf_meta(sforest: WorkspaceForest, delimiter: Optional[str] = None) -> List[Dict[str, str]]:
        """Collects leaf node absolute paths with their corresponding data types."""
        leaf_meta: List[Dict[str, str]] = []
        delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
        default_type = SettingsService.get_default_data_type()

        def _collect(node: HierarchyNode):
            if not node.children:
                leaf_meta.append({"path": node.get_absolute_path(delimiter=delim), "type": node.data_type or default_type})
            else:
                for ch in node.children:
                    _collect(ch)

        for root in sforest.root_nodes:
            _collect(root)
        return leaf_meta

    @staticmethod
    def _build_sheet_forest(
        file_path: str, sheet_name: str, default_type: str, delim: str
    ) -> Tuple[List[str], List[Dict[str, str]], WorkspaceForest]:
        """Reads row 1 headers, maps data types, and builds a populated WorkspaceForest."""
        pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(file_path, sheet_name, default_data_type=default_type)
        h_list = [name for name, _ in pairs]
        type_map = dict(pairs)
        meta = [{"name": name, "type": dtype} for name, dtype in pairs]
        s_forest = PathParserService.parse_header_paths(h_list, delimiter=delim)

        for root in s_forest.root_nodes:
            def _apply(n: HierarchyNode):
                if not n.children:
                    n.data_type = type_map.get(n.get_absolute_path(delimiter=delim)) or type_map.get(n.name) or default_type
                else:
                    for ch in n.children:
                        _apply(ch)
            _apply(root)
        return h_list, meta, s_forest

    def _sync_sheet_forests(self, sheets: List[str], file_path: str, default_type: str, delim: str) -> Dict[str, Any]:
        """Parses row 1 headers across sheets into session forests."""
        all_headers, all_headers_meta = {}, {}
        self.sheet_forests = {}
        for s in sheets:
            h_list, meta, s_forest = self._build_sheet_forest(file_path, s, default_type, delim)
            all_headers[s] = h_list
            all_headers_meta[s] = meta
            self.sheet_forests[s] = s_forest
        return {"all_headers": all_headers, "all_headers_meta": all_headers_meta}

    def import_excel_file(self, file_path: str) -> Dict[str, Any]:
        """Imports Excel file session, reads sheet list, parses Row 1 headers into session forests."""
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        self.current_file_path = file_path
        self.current_template_path = None
        sheets = ExcelHierarchyAdapter.get_sheet_names(file_path)
        if not sheets:
            return {"success": False, "error": "No sheets found in workbook."}
        active_sheet = sheets[0]
        default_type = SettingsService.get_default_data_type()
        delim = SettingsService.get_delimiter()
        sync_res = self._sync_sheet_forests(sheets, file_path, default_type, delim)
        self.current_active_sheet = active_sheet
        self.forest = self.sheet_forests[active_sheet]
        return {
            "success": True,
            "file_path": file_path,
            "sheets": sheets,
            "active_sheet": active_sheet,
            "headers": sync_res["all_headers"].get(active_sheet, []),
            "all_headers": sync_res["all_headers"],
            "headers_meta": sync_res["all_headers_meta"].get(active_sheet, []),
            "all_headers_meta": sync_res["all_headers_meta"],
            "template_path": self.current_template_path,
            "roots": self.forest.to_dict(delimiter=delim)["roots"],
        }

    def refresh_excel_session(self) -> Dict[str, Any]:
        """Reconnects to the currently imported Excel file on disk and updates session forests."""
        if not self.current_file_path:
            return {"success": False, "error": "No active Excel session loaded to refresh."}
        if not os.path.exists(self.current_file_path):
            return {"success": False, "error": f"Cannot refresh: File '{self.current_file_path}' not found."}
        try:
            sheets = ExcelHierarchyAdapter.get_sheet_names(self.current_file_path)
            if not sheets:
                return {"success": False, "error": "Workbook contains no valid worksheets."}
            active_sheet = self.current_active_sheet if self.current_active_sheet in sheets else sheets[0]
            default_type = SettingsService.get_default_data_type()
            delim = SettingsService.get_delimiter()
            sync_res = self._sync_sheet_forests(sheets, self.current_file_path, default_type, delim)
            self.current_active_sheet = active_sheet
            self.forest = self.sheet_forests[active_sheet]
            return {
                "success": True,
                "file_path": self.current_file_path,
                "sheets": sheets,
                "active_sheet": active_sheet,
                "headers": sync_res["all_headers"].get(active_sheet, []),
                "all_headers": sync_res["all_headers"],
                "headers_meta": sync_res["all_headers_meta"].get(active_sheet, []),
                "all_headers_meta": sync_res["all_headers_meta"],
                "template_path": self.current_template_path,
                "roots": self.forest.to_dict(delimiter=delim)["roots"],
            }
        except (FileNotFoundError,):
            return {"success": False, "error": f"Cannot refresh: File '{self.current_file_path}' not found."}
        except (PermissionError, IOError) as e:
            return {"success": False, "error": f"Cannot refresh: File '{self.current_file_path}' is locked ({e})."}
        except Exception as e:
            return {"success": False, "error": f"Cannot refresh Excel session: {str(e)}"}

    def switch_active_sheet(self, sheet_name: str) -> Dict[str, Any]:
        """Switches active sheet, retaining modified tree in session forests."""
        if not self.current_file_path or not os.path.exists(self.current_file_path):
            return {"success": False, "error": "No active Excel session loaded."}
        default_type = SettingsService.get_default_data_type()
        delim = SettingsService.get_delimiter()
        if sheet_name not in self.sheet_forests:
            headers, _, s_forest = self._build_sheet_forest(self.current_file_path, sheet_name, default_type, delim)
            self.sheet_forests[sheet_name] = s_forest
        else:
            headers = ExcelHierarchyAdapter.read_row1_headers(self.current_file_path, sheet_name, default_data_type=default_type)
        self.current_active_sheet = sheet_name
        self.forest = self.sheet_forests[sheet_name]
        return {
            "success": True,
            "sheet_name": sheet_name,
            "headers": headers,
            "template_path": self.current_template_path,
            "roots": self.forest.to_dict(delimiter=delim)["roots"],
        }

    def save_template_sync(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Exports all modified sheet hierarchies to a clean multi-sheet template file."""
        target_path = output_path if output_path else self.current_template_path
        if not target_path:
            if self.current_file_path:
                target_path = os.path.join(os.path.dirname(self.current_file_path), f"Шаблон_{os.path.basename(self.current_file_path)}")
            else:
                target_path = "Шаблон_reorganized_headers_export.xlsx"
        sheet_leaf_paths_map = {sname: self.get_forest_leaf_meta(sforest) for sname, sforest in self.sheet_forests.items()}
        source_file = self.current_file_path if self.current_file_path and os.path.exists(self.current_file_path) else None
        count = ExcelHierarchyAdapter.export_multi_sheet_template(
            file_path_or_stream=source_file, sheet_leaf_paths_map=sheet_leaf_paths_map, output_path=target_path
        )
        self.current_template_path = target_path
        return {
            "success": True,
            "template_path": target_path,
            "total_columns": count,
            "modified_sheets": list(self.sheet_forests.keys()),
        }
