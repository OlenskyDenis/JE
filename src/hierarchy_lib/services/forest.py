"""WorkspaceForest service managing multi-root tree structures."""

from typing import List, Optional, Dict, Any
from src.hierarchy_lib.models.base import HierarchyComponent
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode


class WorkspaceForest:
    """Manages a forest of multiple top-level root nodes and tree manipulations."""

    def __init__(self):
        self.root_nodes: List[CompositeNode] = []

    def add_root(self, node: CompositeNode, index: Optional[int] = None) -> None:
        """Adds a top-level root node to the workspace forest."""
        node.parent = None
        if index is not None and 0 <= index <= len(self.root_nodes):
            self.root_nodes.insert(index, node)
        else:
            self.root_nodes.append(node)

    def remove_root(self, node_id: str) -> Optional[CompositeNode]:
        """Removes a top-level root node by ID."""
        for idx, root in enumerate(self.root_nodes):
            if root.id == node_id:
                return self.root_nodes.pop(idx)
        return None

    def find_node(self, node_id: str) -> Optional[HierarchyComponent]:
        """Recursively finds any node by ID across all root trees in the forest."""
        for root in self.root_nodes:
            found = root.find_node_recursive(node_id)
            if found:
                return found
        return None

    def move_node(self, node_id: str, target_node_id: str, zone: str) -> None:
        """
        Moves a node relative to a target node based on the drag zone:
        - NEST_CHILD: Nest node inside target_node (target must be a container).
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
        if node.is_container and isinstance(node, CompositeNode) and node.is_ancestor_of(target):
            raise ValueError(f"Cannot move parent node '{node.name}' into its own descendant '{target.name}'.")

        # Detach node from current location
        if node.parent:
            if isinstance(node.parent, CompositeNode):
                node.parent.remove_child(node.id)
        else:
            # Was a root node
            self.remove_root(node.id)

        if zone == "NEST_CHILD":
            if not target.is_container or not isinstance(target, CompositeNode):
                raise ValueError(f"Target node '{target.name}' is a leaf node and cannot nest child nodes.")
            target.add_child(node)

        elif zone in ("BEFORE_SIBLING", "AFTER_SIBLING"):
            parent = target.parent
            if parent is not None and isinstance(parent, CompositeNode):
                target_idx = parent.children.index(target)
                insert_idx = target_idx if zone == "BEFORE_SIBLING" else target_idx + 1
                parent.add_child(node, index=insert_idx)
            else:
                # Target is a top-level root node
                target_idx = self.root_nodes.index(target)
                insert_idx = target_idx if zone == "BEFORE_SIBLING" else target_idx + 1
                if not isinstance(node, CompositeNode):
                    # Wrap leaf node in a root container if dropped as a top-level root sibling
                    wrapper = CompositeNode(node.name, node.id)
                    node = wrapper
                self.add_root(node, index=insert_idx)
        else:
            raise ValueError(f"Invalid drag zone '{zone}'. Expected BEFORE_SIBLING, AFTER_SIBLING, or NEST_CHILD.")

    def get_all_leaf_paths(self) -> List[str]:
        """Traverses all trees and collects absolute paths for all leaf nodes across the forest."""
        paths: List[str] = []

        def _traverse(component: HierarchyComponent):
            if not component.is_container or (isinstance(component, CompositeNode) and len(component.children) == 0):
                paths.append(component.get_absolute_path())
            elif isinstance(component, CompositeNode):
                for child in component.children:
                    _traverse(child)

        for root in self.root_nodes:
            _traverse(root)

        return paths

    def to_dict(self) -> Dict[str, Any]:
        return {
            "roots": [root.to_dict() for root in self.root_nodes]
        }
