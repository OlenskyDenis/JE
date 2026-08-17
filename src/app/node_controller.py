"""NodeController handling node CRUD operations and zone mutations on workspace forests."""

from typing import Any, Dict, Optional

from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.settings_service import SettingsService


class NodeController:
    """Controller for dynamic node manipulation, renaming, type updates, deletion, and zone reordering."""

    @staticmethod
    def add_node(
        forest: WorkspaceForest,
        parent_id: Optional[str] = None,
        name: str = "",
        is_container: bool = True,
        target_id: Optional[str] = None,
        zone: Optional[str] = None,
        data_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Adds a new node under parent_id, or relative to target_id and zone, or as a new root node."""
        try:
            delim = SettingsService.get_delimiter()
            default_type = SettingsService.get_default_data_type()
            effective_type = data_type if data_type is not None else default_type
            new_node = HierarchyNode(name, data_type=effective_type)

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
                "roots": forest.to_dict(delimiter=delim)["roots"],
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def move_node(forest: WorkspaceForest, node_id: str, target_node_id: str, zone: str) -> Dict[str, Any]:
        """Moves a node relative to target_node_id based on zone (BEFORE_SIBLING, AFTER_SIBLING, NEST_CHILD)."""
        delim = SettingsService.get_delimiter()
        try:
            forest.move_node(node_id, target_node_id, zone)
            return {"success": True, "rejection_reason": None, "roots": forest.to_dict(delimiter=delim)["roots"]}
        except ValueError as ve:
            return {"success": False, "rejection_reason": str(ve), "roots": forest.to_dict(delimiter=delim)["roots"]}
        except Exception as e:
            return {
                "success": False,
                "rejection_reason": f"Unexpected error: {str(e)}",
                "roots": forest.to_dict(delimiter=delim)["roots"],
            }

    @staticmethod
    def delete_node(forest: WorkspaceForest, node_id: str) -> Dict[str, Any]:
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

            return {"success": True, "roots": forest.to_dict(delimiter=delim)["roots"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_node(
        forest: WorkspaceForest,
        node_id: str,
        name: Optional[str] = None,
        data_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates name and/or data_type of target node in active forest."""
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
                "roots": forest.to_dict(delimiter=delim)["roots"],
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
