"""Eel RPC Bridge methods connecting Python backend with JavaScript frontend."""

import os

# Ensure pure python fallback for gevent if DLL extensions are blocked
os.environ.setdefault("PURE_PYTHON", "1")

from typing import Dict, Any, Optional, List
import eel
from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.adapters.excel_adapter import ExcelHierarchyAdapter
from src.hierarchy_lib.services.dialog_service import FileDialogService
from src.hierarchy_lib.services.path_parser import PathParserService
from src.hierarchy_lib.services.settings_service import SettingsService

# Global active workspace forest instance, multi-sheet session container, and bound paths
forest = WorkspaceForest()
sheet_forests: Dict[str, WorkspaceForest] = {}
current_active_sheet: Optional[str] = None
current_file_path: Optional[str] = None
current_template_path: Optional[str] = None


@eel.expose
def get_settings() -> Dict[str, Any]:
    """Returns current application settings."""
    try:
        settings = SettingsService.get_settings()
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def update_settings(delimiter: Optional[str] = None, default_data_type: Optional[str] = None) -> Dict[str, Any]:
    """Updates application settings and returns recalculated tree roots."""
    global forest, sheet_forests
    try:
        updated = SettingsService.update_settings(delimiter=delimiter, default_data_type=default_data_type)
        return {
            "success": True,
            "settings": updated,
            "roots": forest.to_dict(delimiter=updated["delimiter"])["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def reset_settings() -> Dict[str, Any]:
    """Resets application settings to defaults and returns recalculated tree roots."""
    global forest, sheet_forests
    try:
        reset = SettingsService.reset_to_defaults()
        return {
            "success": True,
            "settings": reset,
            "roots": forest.to_dict(delimiter=reset["delimiter"])["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def add_node(parent_id: Optional[str] = None, name: str = "", is_container: bool = True, target_id: Optional[str] = None, zone: Optional[str] = None, data_type: Optional[str] = "Text") -> Dict[str, Any]:
    """Adds a new dynamic node under parent_id, or relative to target_id and zone, or as a new root node."""
    try:
        delim = SettingsService.get_delimiter()
        new_node = HierarchyNode(name, data_type=data_type)

        if target_id or zone:
            forest.add_node_at_zone(new_node, target_node_id=target_id, zone=zone)
        elif not parent_id:
            forest.add_root(new_node)
        else:
            parent = forest.find_node(parent_id)
            if not parent:
                return {"success": False, "error": f"Parent node '{parent_id}' not found."}
            parent.add_child(new_node)

        return {
            "success": True,
            "node": new_node.to_dict(delimiter=delim),
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def move_node(node_id: str, target_node_id: str, zone: str) -> Dict[str, Any]:
    """
    Moves a node relative to target_node_id based on zone (BEFORE_SIBLING, AFTER_SIBLING, NEST_CHILD).
    Enforces cycle validation and returns updated tree or rejection reason.
    """
    try:
        delim = SettingsService.get_delimiter()
        forest.move_node(node_id, target_node_id, zone)
        return {
            "success": True,
            "rejection_reason": None,
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except ValueError as ve:
        delim = SettingsService.get_delimiter()
        return {
            "success": False,
            "rejection_reason": str(ve),
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        delim = SettingsService.get_delimiter()
        return {
            "success": False,
            "rejection_reason": f"Unexpected error: {str(e)}",
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }


@eel.expose
def delete_node(node_id: str) -> Dict[str, Any]:
    """Deletes a node from the workspace forest."""
    try:
        delim = SettingsService.get_delimiter()
        node = forest.find_node(node_id)
        if not node:
            return {"success": False, "error": "Node not found."}

        if node.parent:
            node.parent.remove_child(node.id)
        else:
            forest.remove_root(node.id)

        return {
            "success": True,
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def update_node(node_id: str, name: Optional[str] = None, data_type: Optional[str] = None) -> Dict[str, Any]:
    """Updates name and/or data_type of target node in active forest."""
    global forest
    try:
        delim = SettingsService.get_delimiter()
        node = forest.find_node(node_id)
        if not node:
            return {"success": False, "error": f"Node '{node_id}' not found."}

        if name is not None:
            trimmed = str(name).strip()
            if not trimmed:
                return {"success": False, "error": "Node name cannot be empty."}
            node.rename(trimmed)

        if data_type is not None:
            node.set_data_type(data_type)

        return {
            "success": True,
            "node": node.to_dict(delimiter=delim),
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_forest_leaf_meta(sforest: WorkspaceForest, delimiter: Optional[str] = None) -> List[Dict[str, str]]:
    """Collects leaf node absolute paths with their corresponding data types."""
    leaf_meta: List[Dict[str, str]] = []
    delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
    default_type = SettingsService.get_default_data_type()

    def _collect(node: HierarchyNode):
        if not node.children:
            leaf_meta.append({
                "path": node.get_absolute_path(delimiter=delim),
                "type": node.data_type or default_type
            })
        else:
            for ch in node.children:
                _collect(ch)

    for root in sforest.root_nodes:
        _collect(root)
    return leaf_meta


@eel.expose
def import_excel_file(file_path: str) -> Dict[str, Any]:
    """Imports Excel file session, reads sheet list, parses Row 1 headers and data types for all sheets into session forests, and returns headers, all_headers, headers_meta, all_headers_meta, and roots."""
    global forest, current_file_path, sheet_forests, current_active_sheet, current_template_path
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        current_file_path = file_path
        current_template_path = None
        sheets = ExcelHierarchyAdapter.get_sheet_names(file_path)
        if not sheets:
            return {"success": False, "error": "No sheets found in workbook."}

        active_sheet = sheets[0]
        all_headers = {}
        all_headers_meta = {}
        sheet_forests = {}
        default_type = SettingsService.get_default_data_type()
        delim = SettingsService.get_delimiter()

        for s in sheets:
            header_type_pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(file_path, s, default_data_type=default_type)
            h_list = [name for name, _ in header_type_pairs]
            type_map = dict(header_type_pairs)
            all_headers[s] = h_list
            all_headers_meta[s] = [
                {"name": name, "type": dtype} for name, dtype in header_type_pairs
            ]
            s_forest = PathParserService.parse_header_paths(h_list, delimiter=delim)
            for root in s_forest.root_nodes:
                def _apply_types(n: HierarchyNode):
                    if not n.children:
                        n.data_type = type_map.get(n.get_absolute_path(delimiter=delim)) or type_map.get(n.name) or default_type
                    else:
                        for ch in n.children:
                            _apply_types(ch)
                _apply_types(root)
            sheet_forests[s] = s_forest

        current_active_sheet = active_sheet
        forest = sheet_forests[active_sheet]
        headers = all_headers.get(active_sheet, [])
        headers_meta = all_headers_meta.get(active_sheet, [])

        return {
            "success": True,
            "file_path": file_path,
            "sheets": sheets,
            "active_sheet": active_sheet,
            "headers": headers,
            "all_headers": all_headers,
            "headers_meta": headers_meta,
            "all_headers_meta": all_headers_meta,
            "template_path": current_template_path,
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def refresh_excel_session() -> Dict[str, Any]:
    """
    Reconnects to the currently imported Excel file on disk, re-parses all sheets' Row 1 headers
    and column formats in streaming mode (max_row=1), and updates session forests and metadata.
    Handles all filesystem, lock, and format exceptions.
    """
    global forest, current_file_path, sheet_forests, current_active_sheet, current_template_path
    if not current_file_path:
        return {"success": False, "error": "No active Excel session loaded to refresh."}

    if not os.path.exists(current_file_path):
        return {"success": False, "error": f"Cannot refresh: File '{current_file_path}' not found."}

    try:
        sheets = ExcelHierarchyAdapter.get_sheet_names(current_file_path)
        if not sheets:
            return {"success": False, "error": "Workbook contains no valid worksheets."}

        # Preserve currently active sheet if present, else fallback to sheets[0]
        active_sheet = current_active_sheet if current_active_sheet in sheets else sheets[0]

        all_headers = {}
        all_headers_meta = {}
        sheet_forests = {}
        default_type = SettingsService.get_default_data_type()
        delim = SettingsService.get_delimiter()

        for s in sheets:
            header_type_pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(current_file_path, s, default_data_type=default_type)
            h_list = [name for name, _ in header_type_pairs]
            type_map = dict(header_type_pairs)
            all_headers[s] = h_list
            all_headers_meta[s] = [
                {"name": name, "type": dtype} for name, dtype in header_type_pairs
            ]
            s_forest = PathParserService.parse_header_paths(h_list, delimiter=delim)
            for root in s_forest.root_nodes:
                def _apply_types(n: HierarchyNode):
                    if not n.children:
                        n.data_type = type_map.get(n.get_absolute_path(delimiter=delim)) or type_map.get(n.name) or default_type
                    else:
                        for ch in n.children:
                            _apply_types(ch)
                _apply_types(root)
            sheet_forests[s] = s_forest

        current_active_sheet = active_sheet
        forest = sheet_forests[active_sheet]
        headers = all_headers.get(active_sheet, [])
        headers_meta = all_headers_meta.get(active_sheet, [])

        return {
            "success": True,
            "file_path": current_file_path,
            "sheets": sheets,
            "active_sheet": active_sheet,
            "headers": headers,
            "all_headers": all_headers,
            "headers_meta": headers_meta,
            "all_headers_meta": all_headers_meta,
            "template_path": current_template_path,
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except (FileNotFoundError,):
        return {"success": False, "error": f"Cannot refresh: File '{current_file_path}' not found."}
    except (PermissionError, IOError) as e:
        return {"success": False, "error": f"Cannot refresh: File '{current_file_path}' is locked by another process or inaccessible ({e})."}
    except Exception as e:
        return {"success": False, "error": f"Cannot refresh Excel session: {str(e)}"}


@eel.expose
def switch_active_sheet(sheet_name: str) -> Dict[str, Any]:
    """Switches active sheet, retaining modified tree in sheet_forests and returning restored roots and headers."""
    global forest, current_file_path, sheet_forests, current_active_sheet, current_template_path
    try:
        if not current_file_path or not os.path.exists(current_file_path):
            return {"success": False, "error": "No active Excel session loaded."}

        default_type = SettingsService.get_default_data_type()
        delim = SettingsService.get_delimiter()

        # If sheet was not yet parsed into sheet_forests, parse from file
        if sheet_name not in sheet_forests:
            header_type_pairs = ExcelHierarchyAdapter.read_row1_headers_and_types(current_file_path, sheet_name, default_data_type=default_type)
            headers = [name for name, _ in header_type_pairs]
            type_map = dict(header_type_pairs)
            s_forest = PathParserService.parse_header_paths(headers, delimiter=delim)
            for root in s_forest.root_nodes:
                def _apply_types(n: HierarchyNode):
                    if not n.children:
                        n.data_type = type_map.get(n.get_absolute_path(delimiter=delim)) or type_map.get(n.name) or default_type
                    else:
                        for ch in n.children:
                            _apply_types(ch)
                _apply_types(root)
            sheet_forests[sheet_name] = s_forest
        else:
            headers = ExcelHierarchyAdapter.read_row1_headers(current_file_path, sheet_name, default_data_type=default_type)

        current_active_sheet = sheet_name
        forest = sheet_forests[sheet_name]

        return {
            "success": True,
            "sheet_name": sheet_name,
            "headers": headers,
            "template_path": current_template_path,
            "roots": forest.to_dict(delimiter=delim)["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def save_template_sync(output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Synchronizes and exports all modified sheet hierarchies in the session to a clean multi-sheet template file.
    Binds current_template_path to target path.
    """
    global current_file_path, current_template_path, sheet_forests
    try:
        target_path = output_path if output_path else current_template_path
        if not target_path:
            if current_file_path:
                base_name = os.path.basename(current_file_path)
                dir_name = os.path.dirname(current_file_path)
                target_path = os.path.join(dir_name, f"Шаблон_{base_name}")
            else:
                target_path = "Шаблон_reorganized_headers_export.xlsx"

        sheet_leaf_paths_map = {}
        for sname, sforest in sheet_forests.items():
            sheet_leaf_paths_map[sname] = get_forest_leaf_meta(sforest)

        source_file = current_file_path if current_file_path and os.path.exists(current_file_path) else None
        count = ExcelHierarchyAdapter.export_multi_sheet_template(
            file_path_or_stream=source_file,
            sheet_leaf_paths_map=sheet_leaf_paths_map,
            output_path=target_path
        )
        current_template_path = target_path
        return {
            "success": True,
            "template_path": target_path,
            "total_columns": count,
            "modified_sheets": list(sheet_forests.keys())
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# Endpoints for Feature 003: Native Desktop File Dialogs

@eel.expose
def open_file_dialog() -> Dict[str, Any]:
    """Opens a native desktop OS file selection dialog for .xlsx files."""
    return FileDialogService.ask_open_file()


@eel.expose
def save_file_dialog(default_name: Optional[str] = None) -> Dict[str, Any]:
    """Opens a native desktop OS save file dialog for choosing destination directory and filename with Шаблон_ prefix."""
    global current_file_path
    if not default_name or default_name == "reorganized_headers_export.xlsx":
        if current_file_path:
            base_name = os.path.basename(current_file_path)
            default_name = f"Шаблон_{base_name}"
        else:
            default_name = "Шаблон_reorganized_headers_export.xlsx"
    return FileDialogService.ask_save_file(default_name=default_name)
