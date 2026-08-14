"""Unified dynamic HierarchyNode class for hierarchical database structures."""

import uuid
from typing import List, Dict, Any, Optional


class HierarchyNode:
    """
    Unified dynamic node component representing both folders and leaves.
    A node with len(children) > 0 dynamically evaluates to a folder (is_folder = True).
    A node with len(children) == 0 dynamically evaluates to a leaf (is_folder = False).
    """

    VALID_DATA_TYPES = (
        "Text",
        "Integer",
        "Decimal",
        "Currency",
        "Percentage",
        "Date",
        "Time",
        "DateTime",
        "Boolean",
    )

    def __init__(self, name: str, node_id: Optional[str] = None, data_type: Optional[str] = "Text"):
        self.id: str = node_id if node_id else str(uuid.uuid4())
        self.name: str = self.sanitize_name(name)
        self.parent: Optional["HierarchyNode"] = None
        self.children: List["HierarchyNode"] = []
        self.data_type: str = self.validate_data_type(data_type) if data_type else "Text"


    @staticmethod
    def sanitize_name(name: str) -> str:
        """Sanitize node name to prevent unescaped backslashes breaking path delimiters."""
        if not name or not str(name).strip():
            return "Unnamed Node"
        clean_name = str(name).strip()
        return clean_name.replace("\\", "/")

    @property
    def is_folder(self) -> bool:
        """Returns True if node has 1 or more children (catalog/folder), False if 0 children (leaf)."""
        return len(self.children) > 0

    @property
    def is_container(self) -> bool:
        """Backwards-compatible alias for is_folder."""
        return self.is_folder

    def is_ancestor_of(self, target: "HierarchyNode") -> bool:
        """Checks if self is equal to target or an ancestor of target (cycle prevention)."""
        if self.id == target.id:
            return True
        current = target.parent
        while current is not None:
            if current.id == self.id:
                return True
            current = current.parent
        return False

    def add_child(self, child: "HierarchyNode", index: Optional[int] = None) -> None:
        """Adds a child component to this node, dynamically upgrading it to a folder."""
        if self.id == child.id or child.is_ancestor_of(self):
            raise ValueError(f"Cannot add ancestor node '{child.name}' as a child of '{self.name}' (cycle detected).")

        # Detach from existing parent if attached elsewhere
        if child.parent and child.parent != self:
            child.parent.remove_child(child.id)

        child.parent = self

        if index is not None and 0 <= index <= len(self.children):
            self.children.insert(index, child)
        else:
            self.children.append(child)

    def remove_child(self, child_id: str) -> Optional["HierarchyNode"]:
        """Removes a child by its ID and unlinks parent pointer, downgrading to leaf if children become empty."""
        for idx, child in enumerate(self.children):
            if child.id == child_id:
                removed = self.children.pop(idx)
                removed.parent = None
                return removed
        return None

    def find_node_recursive(self, node_id: str) -> Optional["HierarchyNode"]:
        """Finds a node by ID anywhere in the subtree rooted at self."""
        if self.id == node_id:
            return self
        for child in self.children:
            found = child.find_node_recursive(node_id)
            if found:
                return found
        return None

    def rename(self, new_name: str) -> None:
        """Renames this node with validation (rejects empty strings / whitespace-only) and strips whitespace."""
        if not new_name or not str(new_name).strip():
            raise ValueError("Node name cannot be empty or whitespace only.")
        self.name = self.sanitize_name(new_name)

    @classmethod
    def validate_data_type(cls, data_type: str) -> str:
        """Validates and returns normalized canonical standard Excel data type string."""
        if not data_type or not str(data_type).strip():
            return "Text"
        clean = str(data_type).strip()
        for valid in cls.VALID_DATA_TYPES:
            if clean.lower() == valid.lower():
                return valid
        raise ValueError(f"Invalid data type '{data_type}'. Expected one of: {', '.join(cls.VALID_DATA_TYPES)}")

    def set_data_type(self, data_type: str) -> None:
        """Sets data type with validation against standard Excel types."""
        self.data_type = self.validate_data_type(data_type)

    def get_absolute_path(self) -> str:
        """Recursively builds backslash-delimited path from root to this node (Root\\Folder\\Item)."""
        if self.parent is None:
            return self.name
        parent_path = self.parent.get_absolute_path()
        return f"{parent_path}\\{self.name}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize node and its children into a dictionary DTO."""
        return {
            "id": self.id,
            "name": self.name,
            "data_type": self.data_type,
            "is_folder": self.is_folder,
            "is_container": self.is_container,
            "absolute_path": self.get_absolute_path(),
            "children": [child.to_dict() for child in self.children]
        }

