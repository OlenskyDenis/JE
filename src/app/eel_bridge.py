"""Eel RPC Bridge router connecting Python backend with JavaScript frontend."""

import os
from typing import Any, Dict, Optional

# Ensure pure python fallback for gevent if DLL extensions are blocked
os.environ.setdefault("PURE_PYTHON", "1")

import eel

from src.app.node_controller import NodeController
from src.app.session_manager import SessionManager
from src.hierarchy_lib.services.dialog_service import FileDialogService
from src.hierarchy_lib.services.settings_service import SettingsService

# Session manager holding multi-sheet forests, active sheet, and template sync state
session = SessionManager()

# Module-level references for direct access and fixture resetting
forest = session.forest
sheet_forests = session.sheet_forests
current_active_sheet = session.current_active_sheet
current_file_path = session.current_file_path
current_template_path = session.current_template_path


def _sync_to_session() -> None:
    """Syncs module-level modifications into session manager."""
    global forest, sheet_forests, current_active_sheet, current_file_path, current_template_path
    if forest is not session.forest:
        session.forest = forest
    if sheet_forests is not session.sheet_forests:
        session.sheet_forests = sheet_forests
    session.current_active_sheet = current_active_sheet
    session.current_file_path = current_file_path
    session.current_template_path = current_template_path


def _sync_from_session() -> None:
    """Syncs session manager state to module-level variables."""
    global forest, sheet_forests, current_active_sheet, current_file_path, current_template_path
    forest = session.forest
    sheet_forests = session.sheet_forests
    current_active_sheet = session.current_active_sheet
    current_file_path = session.current_file_path
    current_template_path = session.current_template_path


@eel.expose
def get_settings() -> Dict[str, Any]:
    """Returns current application settings."""
    try:
        return {"success": True, "settings": SettingsService.get_settings()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def update_settings(delimiter: Optional[str] = None, default_data_type: Optional[str] = None) -> Dict[str, Any]:
    """Updates application settings and returns recalculated tree roots."""
    _sync_to_session()
    try:
        updated = SettingsService.update_settings(delimiter=delimiter, default_data_type=default_data_type)
        return {
            "success": True,
            "settings": updated,
            "roots": session.forest.to_dict(delimiter=updated["delimiter"])["roots"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def reset_settings() -> Dict[str, Any]:
    """Resets application settings to defaults and returns recalculated tree roots."""
    _sync_to_session()
    try:
        reset = SettingsService.reset_to_defaults()
        return {
            "success": True,
            "settings": reset,
            "roots": session.forest.to_dict(delimiter=reset["delimiter"])["roots"],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@eel.expose
def add_node(
    parent_id: Optional[str] = None,
    name: str = "",
    is_container: bool = True,
    target_id: Optional[str] = None,
    zone: Optional[str] = None,
    data_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Adds a new dynamic node under parent_id, relative to target_id and zone, or as a root node."""
    _sync_to_session()
    res = NodeController.add_node(
        forest=session.forest,
        parent_id=parent_id,
        name=name,
        is_container=is_container,
        target_id=target_id,
        zone=zone,
        data_type=data_type,
    )
    _sync_from_session()
    return res


@eel.expose
def move_node(node_id: str, target_node_id: str, zone: str) -> Dict[str, Any]:
    """Moves a node relative to target_node_id based on zone (BEFORE_SIBLING, AFTER_SIBLING, NEST_CHILD)."""
    _sync_to_session()
    res = NodeController.move_node(forest=session.forest, node_id=node_id, target_node_id=target_node_id, zone=zone)
    _sync_from_session()
    return res


@eel.expose
def delete_node(node_id: str) -> Dict[str, Any]:
    """Deletes a node from the active workspace forest."""
    _sync_to_session()
    res = NodeController.delete_node(forest=session.forest, node_id=node_id)
    _sync_from_session()
    return res


@eel.expose
def update_node(node_id: str, name: Optional[str] = None, data_type: Optional[str] = None) -> Dict[str, Any]:
    """Updates name and/or data_type of target node in active forest."""
    _sync_to_session()
    res = NodeController.update_node(forest=session.forest, node_id=node_id, name=name, data_type=data_type)
    _sync_from_session()
    return res


@eel.expose
def import_excel_file(file_path: str) -> Dict[str, Any]:
    """Imports Excel file session, parsing all sheets' Row 1 headers into session forests."""
    res = session.import_excel_file(file_path)
    _sync_from_session()
    return res


@eel.expose
def refresh_excel_session() -> Dict[str, Any]:
    """Reconnects to the currently imported Excel file and updates session forests."""
    _sync_to_session()
    res = session.refresh_excel_session()
    _sync_from_session()
    return res


@eel.expose
def switch_active_sheet(sheet_name: str) -> Dict[str, Any]:
    """Switches active sheet, retaining modified tree in session forests."""
    _sync_to_session()
    res = session.switch_active_sheet(sheet_name)
    _sync_from_session()
    return res


@eel.expose
def save_template_sync(output_path: Optional[str] = None) -> Dict[str, Any]:
    """Exports all modified sheet hierarchies to a clean multi-sheet template file."""
    _sync_to_session()
    res = session.save_template_sync(output_path)
    _sync_from_session()
    return res


@eel.expose
def open_file_dialog() -> Dict[str, Any]:
    """Opens a native desktop OS file selection dialog for .xlsx files."""
    return FileDialogService.ask_open_file()


@eel.expose
def save_file_dialog(default_name: Optional[str] = None) -> Dict[str, Any]:
    """Opens a native desktop OS save file dialog for template output."""
    _sync_to_session()
    if not default_name or default_name == "reorganized_headers_export.xlsx":
        if session.current_file_path:
            base_name = os.path.basename(session.current_file_path)
            default_name = f"Шаблон_{base_name}"
        else:
            default_name = "Шаблон_reorganized_headers_export.xlsx"
    return FileDialogService.ask_save_file(default_name=default_name)
