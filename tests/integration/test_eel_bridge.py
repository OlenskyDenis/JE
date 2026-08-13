"""Integration & contract tests for Eel RPC bridge endpoints."""

import os
import tempfile
import pytest
import openpyxl
import src.app.eel_bridge as bridge


def setup_function():
    """Reset global workspace forest before each test."""
    bridge.forest.root_nodes.clear()


def test_eel_add_and_get_workspace_tree():
    res1 = bridge.add_node(None, "RootA", is_container=True)
    assert res1["success"] is True
    root_id = res1["node"]["id"]

    res2 = bridge.add_node(root_id, "ChildA", is_container=False)
    assert res2["success"] is True

    tree = bridge.get_workspace_tree()
    assert tree["success"] is True
    assert len(tree["roots"]) == 1
    assert tree["roots"][0]["name"] == "RootA"
    assert tree["roots"][0]["children"][0]["name"] == "ChildA"
    assert tree["roots"][0]["children"][0]["absolute_path"] == "RootA\\ChildA"


def test_eel_move_node_cycle_rejection():
    res1 = bridge.add_node(None, "Parent", is_container=True)
    p_id = res1["node"]["id"]

    res2 = bridge.add_node(p_id, "Child", is_container=True)
    c_id = res2["node"]["id"]

    # Attempt to move Parent into Child -> Should reject cycle
    move_res = bridge.move_node(p_id, c_id, "NEST_CHILD")
    assert move_res["success"] is False
    assert "descendant" in move_res["rejection_reason"]


def test_eel_import_export_excel():
    # Setup tree
    res1 = bridge.add_node(None, "Root", is_container=True)
    r_id = res1["node"]["id"]
    bridge.add_node(r_id, "Leaf1", is_container=False)

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Export
        exp_res = bridge.export_excel(tmp_path)
        assert exp_res["success"] is True
        assert exp_res["exported_paths"] == 1

        # Import into fresh state
        bridge.forest.root_nodes.clear()
        imp_res = bridge.import_excel(tmp_path)
        assert imp_res["success"] is True
        assert len(imp_res["roots"]) == 1
        assert imp_res["roots"][0]["name"] == "Root"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
