"""PathParserService for parsing delimited path strings into WorkspaceForest DynamicNode trees."""

from typing import Optional, Sequence
from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.settings_service import SettingsService


class PathParserService:
    """Service providing parsing of hierarchical path strings into a unified WorkspaceForest."""

    @staticmethod
    def parse_header_paths(paths: Sequence[Optional[str]], delimiter: Optional[str] = None) -> WorkspaceForest:
        """
        Parses a sequence of delimited header paths into a WorkspaceForest.
        - Segment separator: supplied delimiter or active SettingsService delimiter (default: '\\')
        - For multi-segment paths (S1\\S2\\...\\Sk): S1 is root node, S2..Sk-1 are intermediate
          nodes (common prefixes are reused), and Sk is a terminal leaf node.
        - For single-segment paths (S1): S1 is created as a root node.
        """
        delim = delimiter if delimiter is not None else SettingsService.get_delimiter()
        forest = WorkspaceForest()
        if not paths:
            return forest

        for raw_path in paths:
            if raw_path is None:
                continue
            path_str = str(raw_path).strip()
            if not path_str:
                continue

            segments = [seg.strip() for seg in path_str.split(delim) if seg.strip()]
            if not segments:
                continue

            root_name = segments[0]

            # Find or create root HierarchyNode
            current_container: Optional[HierarchyNode] = None
            for root in forest.root_nodes:
                if root.name == root_name:
                    current_container = root
                    break

            if current_container is None:
                current_container = HierarchyNode(root_name)
                forest.add_root(current_container)

            # If single segment (e.g. "Status"), it's already a root HierarchyNode
            if len(segments) == 1:
                continue

            # Process intermediate nodes (segments[1:-1])
            for idx in range(1, len(segments) - 1):
                seg_name = segments[idx]
                existing_container = None
                for child in current_container.children:
                    if child.name == seg_name:
                        existing_container = child
                        break

                if existing_container is None:
                    new_container = HierarchyNode(seg_name)
                    current_container.add_child(new_container)
                    current_container = new_container
                else:
                    current_container = existing_container

            # Process terminal leaf node (segments[-1])
            leaf_name = segments[-1]
            existing_leaf = None
            for child in current_container.children:
                if child.name == leaf_name:
                    existing_leaf = child
                    break

            if existing_leaf is None:
                leaf_node = HierarchyNode(leaf_name)
                current_container.add_child(leaf_node)

        return forest
