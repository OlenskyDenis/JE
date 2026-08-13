"""Eel RPC Bridge methods connecting Python backend with JavaScript frontend."""

import os
from typing import Dict, Any, Optional, List
import eel
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.adapters.excel_adapter import ExcelHierarchyAdapter

# Global active workspace forest instance and active file session
forest = WorkspaceForest()
current_file_path: Optional[str] = None


@eel.expose
def get_workspace_tree() -> Dict[str, Any]:
    """Returns full multi-root forest tree dictionary for UI rendering."""
    return {
        "success": True,
        "roots": forest.to_dict()["roots"]
    }


@eel.expose
def add_node(parent_id: Optional[str], name: str, is_container: bool = True) -> Dict[str, Any]:
    """Adds a new node under parent_id or as a new root node if parent_id is None/empty."""
    try:
        new_node = CompositeNode(name) if is_container else LeafNode(name)

        if not parent_id:
            if not isinstance(new_node, CompositeNode):
                # Wrap leaf in container if added at root level
                new_node = CompositeNode(name)
            forest.add_root(new_node)
        else:
            parent = forest.find_node(parent_id)
            if not parent:
                return {"success": False, "error": f"Parent node '{parent_id}' not found."}
            if not parent.is_container or not isinstance(parent, CompositeNode):
                return {"success": False, "error": f"Parent node '{parent.name}' is a leaf node and cannot have children."}
            parent.add_child(new_node)

        return {
            "success": True,
            "node": new_node.to_dict(),
            "roots": forest.to_dict()["roots"]
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
        forest.move_node(node_id, target_node_id, zone)
        return {
            "success": True,
            "rejection_reason": None,
            "roots": forest.to_dict()["roots"]
        }
    except ValueError as ve:
        return {
            "success": False,
            "rejection_reason": str(ve),
            "roots": forest.to_dict()["roots"]
        }
    except Exception as e:
        return {
            "success": False,
            "rejection_reason": f"Unexpected error: {str(e)}",
            "roots": forest.to_dict()["roots"]
        }


@eel.expose
def delete_node(node_id: str) -> Dict[str, Any]:
    """Deletes a node from the workspace forest."""
    try:
        node = forest.find_node(node_id)
        if not node:
            return {"success": False, "error": "Node not found."}

        if node.parent:
            if isinstance(node.parent, CompositeNode):
                node.parent.remove_child(node.id)
        else:
            forest.remove_root(node.id)

        return {
            "success": True,
            "roots": forest.to_dict()["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def import_excel(file_path: str) -> Dict[str, Any]:
    """Imports an Excel file, replacing or merging into the active forest."""
    global forest, current_file_path
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        current_file_path = file_path
        new_forest = ExcelHierarchyAdapter.import_from_file(file_path)
        forest = new_forest
        return {
            "success": True,
            "imported_count": len(forest.root_nodes),
            "roots": forest.to_dict()["roots"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def export_excel(file_path: str) -> Dict[str, Any]:
    """Exports the current forest into an Excel file."""
    try:
        count = ExcelHierarchyAdapter.export_to_file(forest, file_path)
        return {
            "success": True,
            "exported_paths": count
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# New Endpoints for Feature 002: Excel Sidebar Reorganizer

@eel.expose
def import_excel_file(file_path: str) -> Dict[str, Any]:
    """Imports Excel file session, reads sheet list, and returns Row 1 headers for the default first sheet."""
    global current_file_path
    try:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        current_file_path = file_path
        sheets = ExcelHierarchyAdapter.get_sheet_names(file_path)
        if not sheets:
            return {"success": False, "error": "No sheets found in workbook."}

        active_sheet = sheets[0]
        headers = ExcelHierarchyAdapter.read_row1_headers(file_path, active_sheet)

        return {
            "success": True,
            "file_path": file_path,
            "sheets": sheets,
            "active_sheet": active_sheet,
            "headers": headers
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def switch_active_sheet(sheet_name: str) -> Dict[str, Any]:
    """Switches active sheet and returns unique sorted Row 1 headers."""
    global current_file_path
    try:
        if not current_file_path or not os.path.exists(current_file_path):
            return {"success": False, "error": "No active Excel session loaded."}

        headers = ExcelHierarchyAdapter.read_row1_headers(current_file_path, sheet_name)
        return {
            "success": True,
            "sheet_name": sheet_name,
            "headers": headers
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def export_reorganized_row1(sheet_name: str, leaf_paths: List[str], output_path: Optional[str] = None) -> Dict[str, Any]:
    """Exports leaf path strings sequentially into Row 1 horizontally across columns for target sheet."""
    global current_file_path
    try:
        target_path = output_path if output_path else current_file_path
        if not target_path:
            return {"success": False, "error": "No target output path specified."}

        source_file = current_file_path if current_file_path else target_path
        count = ExcelHierarchyAdapter.export_horizontal_row1_leaf_paths(
            file_path_or_stream=source_file,
            sheet_name=sheet_name,
            leaf_paths=leaf_paths,
            output_path=target_path
        )
        return {
            "success": True,
            "column_count": count,
            "output_path": target_path
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
