"""WorkspaceForest service managing multi-root tree structures with dynamic HierarchyNodes."""

from typing import Any, Dict, List, Optional

from src.hierarchy_lib.models.node import HierarchyNode


class WorkspaceForest:
    """Manages a forest of multiple top-level root nodes and tree manipulations."""

    def __init__(self):
        self.root_nodes: List[HierarchyNode] = []

    def add_root(self, node: HierarchyNode, index: Optional[int] = None) -> None:
        """Adds a top-level root node to the workspace forest."""
        node.parent = None
        if index is not None and 0 <= index <= len(self.root_nodes):
            self.root_nodes.insert(index, node)
        else:
            self.root_nodes.append(node)

    def remove_root(self, node_id: str) -> Optional[HierarchyNode]:
        """Removes a top-level root node by ID."""
        for idx, root in enumerate(self.root_nodes):
            if root.id == node_id:
                return self.root_nodes.pop(idx)
        return None

    def find_node(self, node_id: str) -> Optional[HierarchyNode]:
        """Recursively finds any node by ID across all root trees in the forest."""
        for root in self.root_nodes:
            found = root.find_node_recursive(node_id)
            if found:
                return found
        return None

    def add_node_at_zone(
        self, node: HierarchyNode, target_node_id: Optional[str] = None, zone: Optional[str] = None
    ) -> None:
        """
        Inserts a node into the forest relative to target_node_id based on zone.
        If target_node_id or zone is None, appends as a top-level root node.
        Zones:
        - NEST_CHILD: Nest node inside target_node (target dynamically upgrades to folder).
        - BEFORE_SIBLING: Insert node immediately before target_node as a sibling.
        - AFTER_SIBLING: Insert node immediately after target_node as a sibling.
        """
        if not target_node_id or not zone:
            self.add_root(node)
            return

        target = self.find_node(target_node_id)
        if not target:
            raise ValueError(f"Target node '{target_node_id}' not found in workspace forest.")

        if zone == "NEST_CHILD":
            target.add_child(node)

        elif zone in ("BEFORE_SIBLING", "AFTER_SIBLING"):
            parent = target.parent
            if parent is not None:
                target_idx = parent.children.index(target)
                insert_idx = target_idx if zone == "BEFORE_SIBLING" else target_idx + 1
                parent.add_child(node, index=insert_idx)
            else:
                # Target is a top-level root node
                target_idx = self.root_nodes.index(target)
                insert_idx = target_idx if zone == "BEFORE_SIBLING" else target_idx + 1
                self.add_root(node, index=insert_idx)
        else:
            raise ValueError(f"Invalid drag zone '{zone}'. Expected BEFORE_SIBLING, AFTER_SIBLING, or NEST_CHILD.")

    def move_node(self, node_id: str, target_node_id: str, zone: str) -> None:
        """
        Moves a node relative to a target node based on the drag zone:
        - NEST_CHILD: Nest node inside target_node.
        - BEFORE_SIBLING: Insert node immediately before target_node as a sibling.
        - AFTER_SIBLING: Insert node immediately after target_node as a sibling.
        """
        if node_id == target_node_id:
            raise ValueError("Cannot move a node onto itself.")

        node = self.find_node(node_id)
        target = self.find_node(target_node_id)

        if not node or not target:
            raise ValueError("Source or target node not found in workspace forest.")

        # Cycle prevention check
        if node.is_ancestor_of(target):
            raise ValueError(f"Cannot move parent node '{node.name}' into its own descendant '{target.name}'.")

        # Detach node from current location
        if node.parent:
            node.parent.remove_child(node.id)
        else:
            # Was a root node
            self.remove_root(node.id)

        self.add_node_at_zone(node, target_node_id, zone)

    def get_all_leaf_paths(self, delimiter: Optional[str] = None) -> List[str]:
        """Traverses all trees and collects absolute paths for all leaf nodes (nodes with 0 children)."""
        delim = delimiter if delimiter is not None else "\\"
        paths: List[str] = []

        def _traverse(component: HierarchyNode):
            if len(component.children) == 0:
                paths.append(component.get_absolute_path(delimiter=delim))
            else:
                for child in component.children:
                    _traverse(child)

        for root in self.root_nodes:
            _traverse(root)

        return paths

    def to_dict(self, delimiter: Optional[str] = None) -> Dict[str, Any]:
        """Serializes all root trees to dictionary DTO using specified or active delimiter."""
        delim = delimiter if delimiter is not None else "\\"
        return {"roots": [root.to_dict(delimiter=delim) for root in self.root_nodes]}
