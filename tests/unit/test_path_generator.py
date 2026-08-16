"""Unit tests for PathGenerator and WorkspaceForest multi-root tree management."""

import pytest
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode
from src.hierarchy_lib.services.forest import WorkspaceForest
from src.hierarchy_lib.services.path_generator import PathGenerator


def test_multi_root_forest_paths():
    forest = WorkspaceForest()

    # Tree 1
    root1 = CompositeNode("RootA")
    folder1 = CompositeNode("Folder1")
    item1 = LeafNode("Item1")
    folder1.add_child(item1)
    root1.add_child(folder1)
    forest.add_root(root1)

    # Tree 2
    root2 = CompositeNode("RootB")
    item2 = LeafNode("Item2")
    root2.add_child(item2)
    forest.add_root(root2)

    paths = PathGenerator.calculate_all_paths(forest)
    assert len(paths) == 2
    assert "RootA\\Folder1\\Item1" in paths
    assert "RootB\\Item2" in paths


def test_move_node_nest_child():
    forest = WorkspaceForest()

    root1 = CompositeNode("Root1")
    item1 = LeafNode("Item1")
    root1.add_child(item1)
    forest.add_root(root1)

    root2 = CompositeNode("Root2")
    forest.add_root(root2)

    # Move item1 from Root1 into Root2
    forest.move_node(item1.id, root2.id, "NEST_CHILD")

    assert item1.get_absolute_path() == "Root2\\Item1"
    assert len(root1.children) == 0
    assert len(root2.children) == 1

    # Dynamic leaf paths: Root1 (now 0 children) and Root2\Item1 (terminal leaf)
    paths = PathGenerator.calculate_all_paths(forest)
    assert paths == ["Root1", "Root2\\Item1"]


def test_move_node_before_sibling():
    forest = WorkspaceForest()

    root = CompositeNode("Root")
    child1 = LeafNode("Child1")
    child2 = LeafNode("Child2")

    root.add_child(child1)
    root.add_child(child2)
    forest.add_root(root)

    # Move child2 before child1
    forest.move_node(child2.id, child1.id, "BEFORE_SIBLING")

    assert root.children[0].id == child2.id
    assert root.children[1].id == child1.id


def test_calculate_all_paths_custom_delimiter():
    forest = WorkspaceForest()
    root = CompositeNode("Base")
    sub = CompositeNode("Sub")
    leaf = LeafNode("Item")
    sub.add_child(leaf)
    root.add_child(sub)
    forest.add_root(root)

    assert PathGenerator.calculate_path(leaf, delimiter="/") == "Base/Sub/Item"
    assert PathGenerator.calculate_all_paths(forest, delimiter="/") == ["Base/Sub/Item"]
    assert PathGenerator.calculate_path(leaf, delimiter="::") == "Base::Sub::Item"
