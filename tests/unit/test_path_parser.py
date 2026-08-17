"""Unit tests for PathParserService hierarchical path parsing and tree construction."""

from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.path_parser import PathParserService


class TestPathParserService:
    """Test suite verifying PathParserService correctly transforms path strings into HierarchyNode hierarchies."""

    def test_parse_single_nested_path(self):
        """'Root\\Folder\\Leaf' should create Root (folder) -> Folder (folder) -> Leaf (leaf)."""
        paths = [r"Root\Folder\Leaf"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        root = forest.root_nodes[0]
        assert isinstance(root, HierarchyNode)
        assert root.is_folder is True
        assert root.name == "Root"
        assert len(root.children) == 1

        folder = root.children[0]
        assert isinstance(folder, HierarchyNode)
        assert folder.is_folder is True
        assert folder.name == "Folder"
        assert len(folder.children) == 1

        leaf = folder.children[0]
        assert isinstance(leaf, HierarchyNode)
        assert leaf.is_folder is False
        assert leaf.name == "Leaf"
        assert not leaf.is_container
        assert leaf.get_absolute_path() == r"Root\Folder\Leaf"

    def test_parse_shared_prefix_branches_merged(self):
        """Shared parent folders should be merged into single HierarchyNode instances."""
        paths = [r"Company\HR\Employees", r"Company\HR\Salaries", r"Company\Finance\Invoices"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        company = forest.root_nodes[0]
        assert company.name == "Company"
        assert len(company.children) == 2

        hr = next((c for c in company.children if c.name == "HR"), None)
        assert hr is not None
        assert isinstance(hr, HierarchyNode)
        assert hr.is_folder is True
        assert len(hr.children) == 2
        hr_leaves = [c.name for c in hr.children]
        assert "Employees" in hr_leaves
        assert "Salaries" in hr_leaves
        assert all(not c.is_folder for c in hr.children)

        finance = next((c for c in company.children if c.name == "Finance"), None)
        assert finance is not None
        assert isinstance(finance, HierarchyNode)
        assert finance.is_folder is True
        assert len(finance.children) == 1
        assert finance.children[0].name == "Invoices"
        assert finance.children[0].is_folder is False

    def test_parse_single_segment_header(self):
        """Headers without backslash delimiter should create a top-level root node."""
        paths = ["Timestamp", "Status"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 2
        assert forest.root_nodes[0].name == "Timestamp"
        assert forest.root_nodes[1].name == "Status"

    def test_parse_deep_nesting(self):
        """Multi-level deep path (5+ levels) should build complete container chain."""
        paths = [r"A\B\C\D\E\LeafItem"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        curr = forest.root_nodes[0]
        assert curr.name == "A"
        for expected_name in ["B", "C", "D", "E"]:
            assert len(curr.children) == 1
            curr = curr.children[0]
            assert isinstance(curr, HierarchyNode)
            assert curr.is_folder is True
            assert curr.name == expected_name

        assert len(curr.children) == 1
        leaf = curr.children[0]
        assert isinstance(leaf, HierarchyNode)
        assert leaf.is_folder is False
        assert leaf.name == "LeafItem"
        assert leaf.get_absolute_path() == r"A\B\C\D\E\LeafItem"

    def test_whitespace_and_delimiter_cleanup(self):
        """Redundant slashes and extra whitespace around segments should be cleaned properly."""
        paths = [r"  \Root\\SubFolder\  Leaf  \  "]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        root = forest.root_nodes[0]
        assert root.name == "Root"
        assert len(root.children) == 1
        sub = root.children[0]
        assert sub.name == "SubFolder"
        assert len(sub.children) == 1
        leaf = sub.children[0]
        assert leaf.name == "Leaf"
        assert leaf.get_absolute_path() == r"Root\SubFolder\Leaf"

    def test_empty_and_none_paths_ignored(self):
        """Empty strings, whitespace-only, or None values should be gracefully skipped."""
        paths = ["", "   ", None, r"Valid\Path"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        assert forest.root_nodes[0].name == "Valid"
        assert forest.root_nodes[0].children[0].name == "Path"

    def test_duplicate_identical_paths_handled(self):
        """Duplicate identical full paths should not create duplicate identical leaves under the same parent."""
        paths = [r"Root\Folder\Item", r"Root\Folder\Item"]
        forest = PathParserService.parse_header_paths(paths)

        assert len(forest.root_nodes) == 1
        root = forest.root_nodes[0]
        folder = root.children[0]
        assert len(folder.children) == 1
        assert folder.children[0].name == "Item"

    def test_parse_preserves_original_column_order(self):
        """Multi-root trees and child nodes must strictly preserve original encounter sequence."""
        paths = [
            r"Zebra\Stripes\BlackWhite",
            r"Beta\SecondChild",
            r"Alpha\Sub\Item1",
            r"Zebra\Stripes\WhiteBlack",
            r"Beta\FirstChild",
        ]
        forest = PathParserService.parse_header_paths(paths)

        # Roots must be in exact encounter order: Zebra, Beta, Alpha
        assert [r.name for r in forest.root_nodes] == ["Zebra", "Beta", "Alpha"]

        zebra = forest.root_nodes[0]
        stripes = zebra.children[0]
        # Children of Zebra\Stripes: BlackWhite first, WhiteBlack second
        assert [c.name for c in stripes.children] == ["BlackWhite", "WhiteBlack"]

        beta = forest.root_nodes[1]
        # Children of Beta: SecondChild first, FirstChild second
        assert [c.name for c in beta.children] == ["SecondChild", "FirstChild"]

    def test_parse_custom_delimiter_forward_slash(self):
        """Custom delimiter '/' should correctly parse multi-segment paths."""
        paths = ["Company/Engineering/Frontend", "Company/Engineering/Backend", "Sales/Deals"]
        forest = PathParserService.parse_header_paths(paths, delimiter="/")

        assert len(forest.root_nodes) == 2
        company = forest.root_nodes[0]
        assert company.name == "Company"
        eng = company.children[0]
        assert eng.name == "Engineering"
        assert len(eng.children) == 2
        assert eng.children[0].get_absolute_path(delimiter="/") == "Company/Engineering/Frontend"
        assert eng.children[1].get_absolute_path(delimiter="/") == "Company/Engineering/Backend"

    def test_parse_custom_delimiter_double_colon(self):
        """Custom delimiter '::' should correctly parse multi-segment paths."""
        paths = ["Module::Service::Handler", "Module::Service::Router"]
        forest = PathParserService.parse_header_paths(paths, delimiter="::")

        assert len(forest.root_nodes) == 1
        mod = forest.root_nodes[0]
        assert mod.name == "Module"
        svc = mod.children[0]
        assert svc.name == "Service"
        assert [c.name for c in svc.children] == ["Handler", "Router"]
        assert svc.children[0].get_absolute_path(delimiter="::") == "Module::Service::Handler"
