---
name: hierarchy-domain
description: >
  Domain knowledge, business invariants, and Excel data rules for the JE (Database Hierarchy Creator) system.
  Use when modifying tree operations, drag-and-drop mechanics, Excel importing/exporting, data types, or multi-sheet state.
---

# JE Hierarchy & Excel Domain Knowledge Guide

> **Purpose:** Authoritative reference for domain models, business logic invariants, and Excel processing rules in the JE application.

---

## 1. Dynamic Composite Node Model (`HierarchyNode`)

`src/hierarchy_lib/models/node.py`

JE implements a **Dynamic Unified Composite Pattern**:
* A single class `HierarchyNode` acts as both a leaf (terminal element) and a folder (catalog/container).
* **Dynamic Role Evaluation:**
  * `is_folder` / `is_container` is dynamically computed as `len(self.children) > 0`.
  * If a child is added (`add_child`), the node dynamically acts as a folder.
  * If the last child is removed (`remove_child`), the node dynamically degrades back to a leaf.
* **Name Sanitization:**
  * Whitespace is trimmed automatically. Empty/whitespace-only input defaults to `"Unnamed Node"`.
* **Cycle Prevention (`is_ancestor_of`):**
  * Adding a node as its own child or into any of its descendants raises `ValueError`.

### Node DTO Structure (`to_dict`)
```json
{
  "id": "uuid-string",
  "name": "CategoryName",
  "data_type": "Text",
  "is_folder": true,
  "is_container": true,
  "absolute_path": "Root\\CategoryName",
  "children": [...]
}
```

---

## 2. Standard Excel Data Types

`src/hierarchy_lib/models/data_types.py`

JE supports 9 standardized Excel data types:

| Type Name | Default Format String | Description |
|---|---|---|
| `Text` | `@` | Default for string / general text columns |
| `Integer` | `0` | Whole numbers |
| `Decimal` | `0.00` | Floating point / fixed precision |
| `Currency` | `"$"#,##0.00` | Monetary values |
| `Percentage` | `0.00%` | Percentages |
| `Date` | `yyyy-mm-dd` | Calendar dates |
| `Time` | `hh:mm:ss` | Clock times |
| `DateTime` | `yyyy-mm-dd hh:mm:ss` | Timestamps |
| `Boolean` | `General` | True / False flags |

* **Validation:** Case-insensitive normalization via `validate_data_type(type_str)`. Unrecognized types raise `ValueError`.

---

## 3. Workspace Forest Operations (`WorkspaceForest`)

`src/hierarchy_lib/services/forest.py`

* **Multi-Root Container:** Holds a list of top-level root nodes (`root_nodes`).
* **Insertion Zones:**
  * `NEST_CHILD`: Appends `node` to `target.children` (upgrades `target` to folder).
  * `BEFORE_SIBLING`: Inserts `node` immediately before `target` in parent's children or `root_nodes`.
  * `AFTER_SIBLING`: Inserts `node` immediately after `target` in parent's children or `root_nodes`.
* **Safe Move (`move_node`):**
  * Validates source != target.
  * Checks cycle prevention (`is_ancestor_of`).
  * Detaches from old parent/root before inserting at the target zone.
* **Leaf Path Extraction (`get_all_leaf_paths`):**
  * Traverses all trees in depth-first order and returns delimited paths of all nodes where `len(children) == 0`.

---

## 4. Excel Adapter & Streaming Rules (`ExcelHierarchyAdapter`)

`src/hierarchy_lib/adapters/excel_adapter.py`

* **Row 1 Exclusivity:**
  * JE imports **only headers from Row 1** using streaming mode (`max_row=1`).
  * Rows 2+ are never loaded into memory during hierarchy extraction.
* **Header Scanning Termination:**
  * Consecutive empty cell limit: `max_empty_consecutive = 10`. Scanning stops early when reaching 10 contiguous empty columns.
* **Header Deduplication & Ordering:**
  * Deduplicates header names while preserving the original column order.
* **Format Detection (`_map_format_to_data_type`):**
  * Inspects `cell.number_format` and `column_dimensions[col_letter].number_format` to auto-detect one of the 9 data types.
* **Exporting Multi-Sheet Templates (`export_multi_sheet_template`):**
  * Creates a fresh workbook from scratch (`openpyxl.Workbook()`).
  * Writes leaf paths across Row 1 (A1, B1, C1...) and sets appropriate `cell.number_format`.
  * Preserves unmodified sheets by copying their original Row 1 headers without loading data rows.

---

## 5. Delimiters and Settings

`src/hierarchy_lib/services/settings_service.py`

* **Default Delimiter:** `\` (backslash).
* **Allowed Delimiters:** `\`, `/`, `|`, `::`, `->`, or custom single/multi-character strings.
* **Path Parsing:** `PathParserService` converts delimited string paths (e.g. `Finance\Q1\Budget`) into a nested `HierarchyNode` tree.
* **Settings Persistence:** Saved to `settings.json` in workspace root.

---

## 6. Multi-Sheet Session Management

`src/app/eel_bridge.py`

* **Global State:**
  * `forest`: Active `WorkspaceForest` for the currently selected sheet.
  * `sheet_forests`: `Dict[str, WorkspaceForest]` dictionary caching tree states per sheet name.
  * `current_file_path`: Path to active Excel file or `None` if blank canvas.
* **Sheet Switching:**
  * Switching active sheet flushes the current `forest` into `sheet_forests[sheet_name]` and loads the target sheet's forest.
