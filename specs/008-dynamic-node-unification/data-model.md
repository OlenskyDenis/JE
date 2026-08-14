# Domain Data Model: Unified Dynamic HierarchyNode

**Feature**: 008-dynamic-node-unification  
**Date**: 2026-08-14  

## Class Diagram

```
+-------------------------------------------------------------+
|                      WorkspaceForest                        |
| - root_nodes: List[HierarchyNode]                           |
| + add_root(node: HierarchyNode, index: Optional[int])       |
| + remove_root(node_id: str) -> Optional[HierarchyNode]      |
| + find_node(node_id: str) -> Optional[HierarchyNode]        |
| + add_node_at_zone(node, target_node_id, zone)             |
| + move_node(node_id, target_node_id, zone)                  |
| + get_all_leaf_paths() -> List[str]                         |
| + to_dict() -> Dict[str, Any]                               |
+-------------------------------------------------------------+
                              | 1..* (has root nodes)
                              v
+-------------------------------------------------------------+
|                       HierarchyNode                         |
| - id: str (UUID)                                            |
| - name: str                                                 |
| - parent: Optional[HierarchyNode]                           |
| - children: List[HierarchyNode]                             |
+-------------------------------------------------------------+
| + is_folder: bool  -> (len(children) > 0)                   |
| + is_container: bool -> (len(children) > 0)                |
| + add_child(child: HierarchyNode, index: Optional[int])     |
| + remove_child(child_id: str) -> Optional[HierarchyNode]   |
| + find_node_recursive(node_id: str) -> Optional[HierarchyNode]|
| + is_ancestor_of(target: HierarchyNode) -> bool            |
| + get_absolute_path() -> str                                |
| + to_dict() -> Dict[str, Any]                               |
+-------------------------------------------------------------+
```

## DTO JSON Schema (Serialized Representation)

```json
{
  "id": "uuid-v4-string",
  "name": "NodeName",
  "is_folder": true,
  "is_container": true,
  "absolute_path": "Parent\\NodeName",
  "children": [
    {
      "id": "child-uuid",
      "name": "ChildName",
      "is_folder": false,
      "is_container": false,
      "absolute_path": "Parent\\NodeName\\ChildName",
      "children": []
    }
  ]
}
```
