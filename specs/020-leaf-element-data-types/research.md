# Research & Architectural Decisions: Leaf Element Data Type Inspection, Editing, and Excel Persistence

**Feature**: 020-leaf-element-data-types  
**Date**: 2026-08-14  

---

## Decision 1: Excel Data Type Enumeration & openpyxl Format Mappings

- **Context**: Excel cells do not hold arbitrary data types; they use cell data type identifiers (`'s'`, `'n'`, `'d'`, `'b'`, `'f'`) along with specific `number_format` strings. The application needs a clear, standard set of human-readable data types mapped to openpyxl formatting rules.
- **Decision**: Define 9 canonical standard Excel data types:
  1. `Text` -> openpyxl number format `'@'`, data type `'s'`
  2. `Integer` -> openpyxl number format `'0'`, data type `'n'`
  3. `Decimal` -> openpyxl number format `'0.00'`, data type `'n'`
  4. `Currency` -> openpyxl number format `'"$"#,##0.00'` (or `FORMAT_CURRENCY_USD_SIMPLE`), data type `'n'`
  5. `Percentage` -> openpyxl number format `'0.00%'` (or `FORMAT_PERCENTAGE_00`), data type `'n'`
  6. `Date` -> openpyxl number format `'yyyy-mm-dd'` (or `FORMAT_DATE_YYYYMMDD2`), data type `'d'`
  7. `Time` -> openpyxl number format `'hh:mm:ss'`, data type `'d'` / `'n'`
  8. `DateTime` -> openpyxl number format `'yyyy-mm-dd hh:mm:ss'`, data type `'d'`
  9. `Boolean` -> openpyxl number format `'General'`, data type `'b'`
- **Rationale**:
  - Covers 100% of standard Excel spreadsheet column types.
  - Decoupled from COM / Excel installation (Principle V).
  - Clean mapping between frontend UI selectors and openpyxl formatting on workbook export.

---

## Decision 2: Column Type Inference Strategy for Excel Import

- **Context**: When importing an `.xlsx` file, Row 1 contains header names, while actual column types and formats are determined by cell properties across data rows (Rows 2..100).
- **Decision**:
  - `ExcelHierarchyAdapter` scans Row 1 headers to establish columns.
  - For each column, it inspects non-empty cells in Rows 2 through 100 (read-only streaming mode).
  - Type inference heuristics:
    1. If `isinstance(val, bool)` or `cell.data_type == 'b'` -> `Boolean`
    2. If `isinstance(val, datetime.datetime)` or `openpyxl.utils.datetime` date format -> `DateTime` or `Date`
    3. If `isinstance(val, datetime.date)` -> `Date`
    4. If `isinstance(val, datetime.time)` -> `Time`
    5. If number with `$` / currency format -> `Currency`
    6. If number with `%` -> `Percentage`
    7. If integer number / format `'0'` -> `Integer`
    8. If float number / format `'0.00'` -> `Decimal`
    9. Default / Fallback: `Text`
  - Majority consensus across sample rows determines the column's default type.
- **Rationale**: Provides instant, accurate automatic type detection without reading massive files entirely into memory.

---

## Decision 3: Dynamic Composite Node Type Polymorphism (Folder <-> Leaf Transitions)

- **Context**: In this application's dynamic GoF Composite pattern, a node's classification as a folder vs a leaf is dynamic (`is_folder = len(children) > 0`).
- **Decision**:
  - `HierarchyNode` holds `data_type: Optional[str] = "Text"`.
  - When `is_folder` is `True`, `data_type` is considered inactive for UI badge display and column export (because folders are structural groupings, not columns).
  - When a child is deleted or moved away such that `len(children) == 0`:
    - The parent dynamically becomes a leaf (`is_folder = False`).
    - It retains/restores its valid `data_type` (defaulting to `"Text"` if not previously configured).
    - It immediately renders its `.node-type-badge`, enables type editing in `#nodeModal`, and becomes an exportable leaf path.
  - When a node is nested into a leaf (`NEST_CHILD`), the target becomes a folder (`is_folder = True`) and hides its column type badge.
- **Rationale**: Strict adherence to Constitution Principles II & III; eliminates dead-ends and orphaned states.

---

## Decision 4: Sidebar Catalog Type Inheritance and Drag & Drop

- **Context**: When headers are imported into the sidebar catalog, users drag them onto the canvas to construct the hierarchy.
- **Decision**:
  - `import_excel_file` returns header metadata including detected `data_type` (`all_headers_meta`).
  - Catalog items store `data-type` in their DOM attributes and drag payloads.
  - When dropped into the canvas (`handleAddHeaderNode`), `eel.add_node` receives `data_type` and initializes the new leaf node with that detected type.
- **Rationale**: Smooth, frictionless workflow; eliminates repetitive manual type selection for imported columns.

---

## Decision 5: Modal UI Dual-Field Integration (`#nodeModal`)

- **Context**: Users need to view and edit both node name and node data type without UI clutter.
- **Decision**:
  - Add `#selectNodeType` container to `#nodeModal`.
  - In `'edit'` mode for leaf nodes: both Name input and Data Type select are visible and pre-selected.
  - In `'edit'` mode for folder nodes: Data Type selector is hidden/disabled with a clear hint: *"Data types apply to leaf data elements only"*.
  - In `'create'` mode: Data Type selector defaults to `Text` (or is hidden until created).
- **Rationale**: Reuses the existing tested modal with zero DOM bloat or visual shifting.
