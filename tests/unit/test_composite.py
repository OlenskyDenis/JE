"""Unit tests for GoF Composite Pattern classes (HierarchyComponent, CompositeNode, LeafNode)."""

import pytest
from src.hierarchy_lib.models.composite import CompositeNode
from src.hierarchy_lib.models.leaf import LeafNode


def test_leaf_node_creation():
    leaf = LeafNode("Item1")
    assert leaf.name == "Item1"
    assert leaf.is_container is False
    assert leaf.get_absolute_path() == "Item1"


def test_composite_node_hierarchy_building():
    root = CompositeNode("Root")
    folder = CompositeNode("Folder")
    subfolder = CompositeNode("Subfolder")
    item = LeafNode("Item")

    subfolder.add_child(item)
    folder.add_child(subfolder)
    root.add_child(folder)

    assert item.get_absolute_path() == "Root\\Folder\\Subfolder\\Item"
    assert subfolder.get_absolute_path() == "Root\\Folder\\Subfolder"
    assert folder.get_absolute_path() == "Root\\Folder"
    assert root.get_absolute_path() == "Root"


def test_cycle_prevention_direct_self():
    node = CompositeNode("NodeA")
    with pytest.raises(ValueError, match="cycle detected"):
        node.add_child(node)


def test_cycle_prevention_ancestor_to_descendant():
    root = CompositeNode("Root")
    child = CompositeNode("Child")
    grandchild = CompositeNode("Grandchild")

    root.add_child(child)
    child.add_child(grandchild)

    # Attempt to add 'root' as a child of 'grandchild'
    with pytest.raises(ValueError, match="cycle detected"):
        grandchild.add_child(root)


def test_remove_child():
    root = CompositeNode("Root")
    item = LeafNode("Item")
    root.add_child(item)

    assert len(root.children) == 1
    removed = root.remove_child(item.id)
    assert removed.id == item.id
    assert len(root.children) == 0
    assert item.parent is None
