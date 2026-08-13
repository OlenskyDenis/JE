"""LeafNode class for GoF Composite Pattern representing terminal nodes."""

from typing import Dict, Any, Optional
from src.hierarchy_lib.models.base import HierarchyComponent


class LeafNode(HierarchyComponent):
    """Concrete Leaf component in Composite pattern representing terminal items."""

    def __init__(self, name: str, node_id: Optional[str] = None):
        super().__init__(name, node_id)

    @property
    def is_container(self) -> bool:
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "is_container": False,
            "absolute_path": self.get_absolute_path(),
            "children": []
        }
