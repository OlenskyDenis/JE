"""Unit tests for WorkspaceForest.add_node_at_zone positional insertion with dynamic HierarchyNodes."""

from src.hierarchy_lib.models.node import HierarchyNode
from src.hierarchy_lib.services.forest import WorkspaceForest


def test_add_node_at_zone_root_level():
    forest = WorkspaceForest()
    root1 = HierarchyNode("Root1")
    root2 = HierarchyNode("Root2")
    forest.add_root(root1)
    forest.add_root(root2)

    # Insert new node BEFORE root2 as sibling
    new_leaf = HierarchyNode("NewHeaderBefore")
    forest.add_node_at_zone(new_leaf, target_node_id=root2.id, zone="BEFORE_SIBLING")

    assert len(forest.root_nodes) == 3
    assert forest.root_nodes[0].name == "Root1"
    assert forest.root_nodes[1].name == "NewHeaderBefore"
    assert forest.root_nodes[2].name == "Root2"

    # Insert new node AFTER root2 as sibling
    new_leaf2 = HierarchyNode("NewHeaderAfter")
    forest.add_node_at_zone(new_leaf2, target_node_id=root2.id, zone="AFTER_SIBLING")

    assert len(forest.root_nodes) == 4
    assert forest.root_nodes[2].name == "Root2"
    assert forest.root_nodes[3].name == "NewHeaderAfter"


def test_add_node_at_zone_inside_container():
    forest = WorkspaceForest()
    root = HierarchyNode("Root")
    folder = HierarchyNode("Folder")
    root.add_child(folder)
    forest.add_root(root)

    # Insert new leaf node inside Folder using NEST_CHILD
    item1 = HierarchyNode("Item1")
    forest.add_node_at_zone(item1, target_node_id=folder.id, zone="NEST_CHILD")

    assert len(folder.children) == 1
    assert folder.children[0].name == "Item1"

    # Insert item2 BEFORE item1 as sibling
    item0 = HierarchyNode("Item0")
    forest.add_node_at_zone(item0, target_node_id=item1.id, zone="BEFORE_SIBLING")

    # Insert item3 AFTER item1 as sibling
    item2 = HierarchyNode("Item2")
    forest.add_node_at_zone(item2, target_node_id=item1.id, zone="AFTER_SIBLING")

    assert [c.name for c in folder.children] == ["Item0", "Item1", "Item2"]


def test_add_node_at_zone_nest_child_on_leaf_upgrades_to_folder():
    """Nesting a child onto a leaf node (0 children) succeeds and dynamically upgrades it to a folder."""
    forest = WorkspaceForest()
    root = HierarchyNode("Root")
    leaf = HierarchyNode("Leaf")
    root.add_child(leaf)
    forest.add_root(root)

    assert leaf.is_folder is False
    assert leaf.is_container is False

    new_item = HierarchyNode("NewItem")
    forest.add_node_at_zone(new_item, target_node_id=leaf.id, zone="NEST_CHILD")

    assert leaf.is_folder is True
    assert leaf.is_container is True
    assert len(leaf.children) == 1
    assert leaf.children[0].name == "NewItem"
    assert leaf.children[0].get_absolute_path() == "Root\\Leaf\\NewItem"
