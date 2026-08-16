"""Abstract base component for GoF Composite Pattern."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import uuid


class HierarchyComponent(ABC):
    """Abstract Component interface unifying containers (CompositeNode) and leaves (LeafNode)."""

    def __init__(self, name: str, node_id: Optional[str] = None):
        self.id: str = node_id if node_id else str(uuid.uuid4())
        self.name: str = self.sanitize_name(name)
        self.parent: Optional["HierarchyComponent"] = None

    @staticmethod
    def sanitize_name(name: str) -> str:
        """Sanitize node name to prevent unescaped backslashes breaking path delimiters."""
        if not name or not name.strip():
            return "Unnamed Node"
        # Trim leading/trailing whitespace
        clean_name = name.strip()
        # Replace raw backslashes with forward slashes or escaped representation if present inside name
        return clean_name.replace("\\", "/")

    def get_absolute_path(self, delimiter: Optional[str] = None) -> str:
        """Recursively builds delimited path from root to this component (Root\\Folder\\Item)."""
        delim = delimiter if delimiter is not None else "\\"
        if self.parent is None:
            return self.name
        parent_path = self.parent.get_absolute_path(delimiter=delim)
        return f"{parent_path}{delim}{self.name}"

    @property
    @abstractmethod
    def is_container(self) -> bool:
        """Returns True if component is a CompositeNode, False if LeafNode."""
        pass

    @abstractmethod
    def to_dict(self, delimiter: Optional[str] = None) -> Dict[str, Any]:
        """Serialize node and its children into a dictionary DTO."""
        pass
