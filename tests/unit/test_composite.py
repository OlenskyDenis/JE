"""Unit tests for unified dynamic HierarchyNode."""

import pytest

from src.hierarchy_lib.models.node import HierarchyNode


def test_hierarchy_node_initial_leaf_state():
    """A newly created HierarchyNode with 0 children is dynamically treated as a leaf."""
    node = HierarchyNode("Item1")
    assert node.name == "Item1"
    assert node.is_folder is False
    assert node.is_container is False
    assert len(node.children) == 0
    assert node.get_absolute_path() == "Item1"


def test_hierarchy_node_dynamic_upgrade_to_folder():
    """Adding a child automatically upgrades a node to a folder (is_folder = True)."""
    parent = HierarchyNode("Parent")
    assert parent.is_folder is False
    assert parent.is_container is False

    child = HierarchyNode("Child")
    parent.add_child(child)

    assert parent.is_folder is True
    assert parent.is_container is True
    assert child.is_folder is False
    assert child.is_container is False
    assert child.get_absolute_path() == "Parent\\Child"


def test_hierarchy_node_dynamic_downgrade_to_leaf():
    """Removing the last child automatically downgrades a folder back to a leaf."""
    parent = HierarchyNode("Parent")
    child = HierarchyNode("Child")
    parent.add_child(child)
    assert parent.is_folder is True

    removed = parent.remove_child(child.id)
    assert removed.id == child.id
    assert child.parent is None
    assert parent.is_folder is False
    assert parent.is_container is False
    assert len(parent.children) == 0


def test_hierarchy_node_multi_level_building():
    root = HierarchyNode("Root")
    folder = HierarchyNode("Folder")
    subfolder = HierarchyNode("Subfolder")
    item = HierarchyNode("Item")

    subfolder.add_child(item)
    folder.add_child(subfolder)
    root.add_child(folder)

    assert item.get_absolute_path() == "Root\\Folder\\Subfolder\\Item"
    assert subfolder.get_absolute_path() == "Root\\Folder\\Subfolder"
    assert folder.get_absolute_path() == "Root\\Folder"
    assert root.get_absolute_path() == "Root"

    assert root.is_folder is True
    assert folder.is_folder is True
    assert subfolder.is_folder is True
    assert item.is_folder is False


def test_cycle_prevention_direct_self():
    node = HierarchyNode("NodeA")
    with pytest.raises(ValueError, match="cycle detected"):
        node.add_child(node)


def test_cycle_prevention_ancestor_to_descendant():
    root = HierarchyNode("Root")
    child = HierarchyNode("Child")
    grandchild = HierarchyNode("Grandchild")

    root.add_child(child)
    child.add_child(grandchild)

    # Attempt to add 'root' as a child of 'grandchild'
    with pytest.raises(ValueError, match="cycle detected"):
        grandchild.add_child(root)


def test_hierarchy_node_serialization():
    root = HierarchyNode("Root")
    child = HierarchyNode("LeafChild")
    root.add_child(child)

    d = root.to_dict()
    assert d["name"] == "Root"
    assert d["is_folder"] is True
    assert d["is_container"] is True
    assert len(d["children"]) == 1

    c = d["children"][0]
    assert c["name"] == "LeafChild"
    assert c["is_folder"] is False
    assert c["is_container"] is False
    assert len(c["children"]) == 0


def test_hierarchy_node_rename():
    node = HierarchyNode("OldName")
    assert node.name == "OldName"

    # Valid rename with whitespace trimming
    node.rename("  NewName  ")
    assert node.name == "NewName"

    # Child path propagation after parent rename
    child = HierarchyNode("ChildItem")
    node.add_child(child)
    assert child.get_absolute_path() == "NewName\\ChildItem"

    node.rename("ParentCategory")
    assert child.get_absolute_path() == "ParentCategory\\ChildItem"

    # Empty string and whitespace-only rejections
    with pytest.raises(ValueError, match="cannot be empty"):
        node.rename("")

    with pytest.raises(ValueError, match="cannot be empty"):
        node.rename("   ")

    # Name remains unchanged on rejected rename
    assert node.name == "ParentCategory"


def test_hierarchy_node_data_type_defaults_and_mutation():
    """HierarchyNode defaults to Text data_type and allows mutation to standard Excel types."""
    node = HierarchyNode("Item1")
    assert node.data_type == "Text"

    # Mutate to standard types
    node.set_data_type("Currency")
    assert node.data_type == "Currency"

    node.set_data_type("Date")
    assert node.data_type == "Date"

    node.set_data_type("Integer")
    assert node.data_type == "Integer"

    # Reject invalid data types
    with pytest.raises(ValueError, match="Invalid data type"):
        node.set_data_type("UnsupportedType")


def test_hierarchy_node_serialization_with_data_type():
    """Serialization includes data_type attribute."""
    node = HierarchyNode("Price", data_type="Currency")
    d = node.to_dict()
    assert d["name"] == "Price"
    assert d["data_type"] == "Currency"


def test_hierarchy_node_folder_to_leaf_data_type_lifecycle():
    """When a folder loses all children, it transitions to leaf and retains valid data_type."""
    parent = HierarchyNode("Category", data_type="Text")
    child = HierarchyNode("Item", data_type="Decimal")
    parent.add_child(child)

    assert parent.is_folder is True

    # Remove child -> parent transitions back to leaf
    parent.remove_child(child.id)
    assert parent.is_folder is False
    assert parent.data_type == "Text"
    d = parent.to_dict()
    assert d["is_folder"] is False
    assert d["data_type"] == "Text"
