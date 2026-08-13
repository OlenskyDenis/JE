"""CompositeNode class for GoF Composite Pattern managing child components."""

from typing import List, Dict, Any, Optional
from src.hierarchy_lib.models.base import HierarchyComponent


class CompositeNode(HierarchyComponent):
    """Concrete Composite component managing child HierarchyComponent instances."""

    def __init__(self, name: str, node_id: Optional[str] = None):
        super().__init__(name, node_id)
        self.children: List[HierarchyComponent] = []

    @property
    def is_container(self) -> bool:
        return True

    def is_ancestor_of(self, target: HierarchyComponent) -> bool:
        """Checks if self is equal to target or an ancestor of target (cycle prevention)."""
        if self.id == target.id:
            return True
        current = target.parent
        while current is not None:
            if current.id == self.id:
                return True
            current = current.parent
        return False

    def add_child(self, child: HierarchyComponent, index: Optional[int] = None) -> None:
        """Adds a child component to this container, setting its parent reference."""
        # Cycle prevention check: self cannot be child itself, and an ancestor cannot become a child
        if self.id == child.id or (isinstance(child, CompositeNode) and child.is_ancestor_of(self)):
            raise ValueError(f"Cannot add ancestor node '{child.name}' as a child of '{self.name}' (cycle detected).")

        # Detach from existing parent if attached elsewhere
        if child.parent and child.parent != self:
            if isinstance(child.parent, CompositeNode):
                child.parent.remove_child(child.id)

        child.parent = self

        if index is not None and 0 <= index <= len(self.children):
            self.children.insert(index, child)
        else:
            self.children.append(child)

    def remove_child(self, child_id: str) -> Optional[HierarchyComponent]:
        """Removes a child by its ID and unlinks parent pointer."""
        for idx, child in enumerate(self.children):
            if child.id == child_id:
                removed = self.children.pop(idx)
                removed.parent = None
                return removed
        return None

    def find_node_recursive(self, node_id: str) -> Optional[HierarchyComponent]:
        """Finds a node by ID anywhere in the subtree rooted at self."""
        if self.id == node_id:
            return self
        for child in self.children:
            if child.id == node_id:
                return child
            if child.is_container and isinstance(child, CompositeNode):
                found = child.find_node_recursive(node_id)
                if found:
                    return found
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "is_container": True,
            "absolute_path": self.get_absolute_path(),
            "children": [child.to_dict() for child in self.children]
        }
