"""PathGenerator service for calculating and formatting backslash-separated absolute node paths."""

from typing import List
from src.hierarchy_lib.models.base import HierarchyComponent
from src.hierarchy_lib.services.forest import WorkspaceForest


class PathGenerator:
    """Service responsible for generating and formatting backslash absolute paths."""

    @staticmethod
    def calculate_path(component: HierarchyComponent) -> str:
        """Returns the absolute backslash-separated path for a given node component."""
        return component.get_absolute_path()

    @staticmethod
    def calculate_all_paths(forest: WorkspaceForest) -> List[str]:
        """Returns all leaf paths across all root nodes in the workspace forest."""
        return forest.get_all_leaf_paths()
