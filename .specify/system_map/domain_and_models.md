# Domain & Models Layer: Pure Business Logic

**Path**: `.specify/system_map/domain_and_models.md`  
**Architectural Layer**: Model / Domain Core  
**Governing Principles**: Constitution Principle II (SOLID & DIP) & Principle III (Dynamic Composite)

---

## 1. Responsibilities & Invariants

The Domain layer encapsulates the core hierarchical data structures and business rules for the JE application. It is pure Python, completely independent of UI frameworks, RPC bridges, or persistence storage.

### Key Invariants:
1. **Dynamic Composite (GoF)**: A node is dynamically evaluated as a folder (`is_folder = True`) if and only if `len(children) > 0`. A node with 0 children is dynamically a leaf (`is_folder = False`).
2. **Cycle Prevention**: A node cannot be added or moved as a child of its own descendant or itself (`node.is_ancestor_of(target)`).
3. **Dependency Inversion (DIP)**: Domain models **NEVER** import infrastructure services (`SettingsService`, `ExcelHierarchyAdapter`, or `eel_bridge`). All configuration (e.g. `delimiter`, `data_type`) is passed into methods with default fallbacks (`delimiter: str = "\\"`, `default_data_type: str = "Text"`).

---

## 2. Component Inventory

### 2.1 [`HierarchyNode`](file:///E:/JE/src/hierarchy_lib/models/node.py)
* **File**: `src/hierarchy_lib/models/node.py`
* **Role**: Universal dynamic tree component unifying leaves and folders.
* **Attributes**:
  * `id: str` (UUID string)
  * `name: str` (Sanitized non-empty string)
  * `parent: Optional[HierarchyNode]` (Pointer to parent or `None` for root)
  * `children: List[HierarchyNode]` (Ordered list of child nodes)
  * `data_type: str` (One of the 9 standard Excel data types)
* **Core Methods**:
  * `add_child(child, index=None)`: Attaches child with cycle detection, sets `child.parent = self`.
  * `remove_child(child_id)`: Unlinks child, sets `child.parent = None`.
  * `rename(new_name)`: Validates and updates node name with whitespace trimming.
  * `set_data_type(data_type)`: Validates and updates data type via `data_types.py`.
  * `get_absolute_path(delimiter="\\")`: Recursively builds full hierarchical path.
  * `to_dict(delimiter="\\")`: Serializes subtree into `HierarchyNodeDTO`.

### 2.2 [`data_types.py`](file:///E:/JE/src/hierarchy_lib/models/data_types.py)
* **File**: `src/hierarchy_lib/models/data_types.py`
* **Role**: Single source of truth (OCP) for standard Excel column data types and validation.
* **Constants**:
  * `VALID_DATA_TYPES`: `("Text", "Integer", "Decimal", "Currency", "Percentage", "Date", "Time", "DateTime", "Boolean")`
* **Functions**:
  * `validate_data_type(data_type: str) -> str`: Normalizes case-insensitively to canonical title or raises `ValueError`.

### 2.3 [`WorkspaceForest`](file:///E:/JE/src/hierarchy_lib/services/forest.py)
* **File**: `src/hierarchy_lib/services/forest.py`
* **Role**: Multi-root canvas tree container managing independent top-level root nodes.
* **Attributes**:
  * `root_nodes: List[HierarchyNode]` (Ordered list of root trees)
* **Core Methods**:
  * `add_root(node, index=None)`: Appends or inserts a top-level root tree.
  * `remove_root(node_id)`: Removes a top-level root.
  * `find_node(node_id)`: Recursive subtree search across all roots in the forest.
  * `add_node_at_zone(node, target_node_id, zone)`: Positional insertion relative to target (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`).
  * `move_node(node_id, target_node_id, zone)`: Cycle-validated movement across roots or branches.
  * `get_all_leaf_paths(delimiter="\\")`: Deep traversal collecting all terminal leaf absolute paths.
  * `to_dict(delimiter="\\")`: Serializes all root trees into `WorkspaceForestDTO`.

### 2.4 [`PathParserService`](file:///E:/JE/src/hierarchy_lib/services/path_parser.py)
* **File**: `src/hierarchy_lib/services/path_parser.py`
* **Role**: Pure path parsing engine transforming sequences of delimited strings into `WorkspaceForest`.
* **Core Methods**:
  * `parse_header_paths(paths: Sequence[Optional[str]], delimiter="\\") -> WorkspaceForest`:
    * Parses segments using `delimiter`.
    * Reuses common parent containers for shared prefixes.
    * Creates single-segment paths as root nodes.
    * Preserves original column encounter order.

---

## 3. Retired Entities & Historical Removals

| Entity | Formerly | Reason for Retirement | Replaced By |
|---|---|---|---|
| `HierarchyComponent` | `models/base.py` | Over-abstracted base class breaking custom delimiter paths (`/` vs `\`). | `HierarchyNode` directly |
| `CompositeNode` | `models/composite.py` | Redundant class alias. | `HierarchyNode` |
| `LeafNode` | `models/leaf.py` | Redundant class alias. | `HierarchyNode` |
| `PathGenerator` | `services/path_generator.py` | Static utility duplicate. | `HierarchyNode.get_absolute_path()` & `WorkspaceForest.get_all_leaf_paths()` |
