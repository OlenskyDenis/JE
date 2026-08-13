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

    def get_absolute_path(self) -> str:
        """Recursively builds backslash-delimited path from root to this component (Root\\Folder\\Item)."""
        if self.parent is None:
            return self.name
        parent_path = self.parent.get_absolute_path()
        return f"{parent_path}\\{self.name}"

    @property
    @abstractmethod
    def is_container(self) -> bool:
        """Returns True if component is a CompositeNode, False if LeafNode."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize node and its children into a dictionary DTO."""
        pass
