# Domain Data Model: Hierarchical Excel Header Parser

**Feature**: 006-excel-hierarchical-import  
**Date**: 2026-08-14  

## Domain Entities

```
+-------------------------------------------------------------+
|                      WorkspaceForest                        |
| - root_nodes: List[CompositeNode]                           |
+-------------------------------------------------------------+
                              | 1..* (has roots)
                              v
+-------------------------------------------------------------+
|                     HierarchyComponent                      |
| - id: str (UUID)                                            |
| - name: str                                                 |
| - parent: Optional[HierarchyComponent]                      |
| + get_absolute_path() -> str                                |
| + to_dict() -> Dict[str, Any]                               |
+-------------------------------------------------------------+
           ^                                       ^
           | (is a)                                | (is a)
+-----------------------+              +-----------------------+
|     CompositeNode     |              |       LeafNode        |
| - children: List[...] |              | - is_container: False |
| - is_container: True  |              +-----------------------+
+-----------------------+
```

### 1. `PathParserService`

Service responsible for transforming a collection of raw path strings into a unified `WorkspaceForest`.

```python
class PathParserService:
    @staticmethod
    def parse_header_paths(paths: List[str]) -> WorkspaceForest:
        """Parses backslash path strings into a populated WorkspaceForest."""
        ...
```

### 2. Node Mapping Rules

| Path Pattern | Example | Resulting Hierarchy |
|---|---|---|
| Multi-segment ($k \ge 2$) | `Root\Folder\Leaf` | Root (Composite) $\rightarrow$ Folder (Composite) $\rightarrow$ Leaf (LeafNode) |
| Shared prefix | `Root\Folder\L1`, `Root\Folder\L2` | Root (Composite) $\rightarrow$ Folder (Composite) $\rightarrow$ [L1, L2] |
| Single-segment ($k = 1$) | `SingleColumn` | SingleColumn (CompositeNode root) |
| Deep nesting ($k = 4$) | `A\B\C\D` | A $\rightarrow$ B $\rightarrow$ C $\rightarrow$ D (LeafNode) |
