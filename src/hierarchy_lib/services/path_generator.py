"""PathGenerator service for calculating and formatting delimited absolute node paths."""

from typing import List, Optional
from src.hierarchy_lib.models.base import HierarchyComponent
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.settings_service import SettingsService


class PathGenerator:
    """Service responsible for generating and formatting delimited absolute paths."""

    @staticmethod
    def calculate_path(component: HierarchyComponent, delimiter: Optional[str] = None) -> str:
        """Returns the absolute delimited path for a given node component."""
        delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
        return component.get_absolute_path(delimiter=delim)

    @staticmethod
    def calculate_all_paths(forest: WorkspaceForest, delimiter: Optional[str] = None) -> List[str]:
        """Returns all leaf paths across all root nodes in the workspace forest."""
        delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
        return forest.get_all_leaf_paths(delimiter=delim)
