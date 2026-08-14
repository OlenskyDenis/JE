# Research & Architectural Decisions: Dynamic HierarchyNode Unification

**Feature**: 008-dynamic-node-unification  
**Date**: 2026-08-14  

## Decision 1: Unified `HierarchyNode` Class

- **Context**: The codebase previously used separate `CompositeNode` and `LeafNode` subclasses inheriting from abstract `HierarchyComponent`. This caused rigid typing constraints where a `LeafNode` could not receive children without being replaced or re-instantiated.
- **Decision**: Unify into a single `HierarchyNode` class in `src/hierarchy_lib/models/node.py` (and maintain aliases `CompositeNode = HierarchyNode`, `LeafNode = HierarchyNode` for backwards compatibility).
- **Core Attributes**:
  - `id: str`: UUID string identifier
  - `name: str`: Cleaned string name
  - `parent: Optional[HierarchyNode]`: Parent node reference
  - `children: List[HierarchyNode]`: List of child nodes
- **Dynamic Properties**:
  - `is_folder: bool` $\rightarrow$ `len(self.children) > 0`
  - `is_container: bool` $\rightarrow$ `len(self.children) > 0` (property alias)

## Decision 2: Dynamic State Transitions

- **Adding a Child**: Calling `node.add_child(child)` appends the child and sets `child.parent = node`. If `node` previously had 0 children, `node.is_folder` dynamically transitions from `False` to `True`.
- **Removing a Child**: Calling `node.remove_child(child_id)` removes the child and sets `child.parent = None`. If `node.children` becomes empty, `node.is_folder` dynamically transitions from `True` to `False`.

## Decision 3: Universal Drag-and-Drop & Nesting

- **Context**: Previously, dropping with `NEST_CHILD` on a `LeafNode` was rejected by backend validation (`Target node is a leaf node and cannot nest child nodes`).
- **Decision**: `WorkspaceForest.add_node_at_zone` and `move_node` now allow `NEST_CHILD` on any valid target `HierarchyNode`.
- **Cycle Prevention**: Retain strict cycle validation (`if node == target or node.is_ancestor_of(target): raise ValueError("Cannot move ancestor into descendant")`).

## Decision 4: Frontend UI Dynamic Rendering (`tree_renderer.js`)

- Every node renders with:
  - Dynamic icon: Folder icon if `node.children && node.children.length > 0`, Leaf icon if 0 children.
  - Universal `+ Add Child` action button so any node can be expanded into a catalog folder.
  - Delete button.
  - Nested children list if `node.children && node.children.length > 0`.
