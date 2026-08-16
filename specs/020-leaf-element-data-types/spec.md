# Feature Specification: Leaf Element Data Type Inspection, Editing, and Excel Persistence

**Feature Branch**: `020-leaf-element-data-types`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "Add new functionality for viewing and editing each element that is not a folder in the Hierarchy Constructor Workspace, so that the element type can be viewed and edited; the types should be pulled from Excel by default, based on the column type and value type, and similarly, when editing the value type, the type in Excel should update upon saving; allow users to select from all standard types available in Excel."  
**Clarification Addendum**: Account for dynamic folder-to-leaf conversion upon child deletion/movement, full system map audit, sidebar catalog data type inheritance, and export preview type visualization.

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is created, edited, or deleted.
- **Principle II (OOP & Clean State Architecture)**:
  - Clean Domain Encapsulation: `HierarchyNode` encapsulates `data_type` state with validation against standard Excel types.
  - Folder/Leaf Segregation: Folder nodes (`is_folder = True`, `len(children) > 0`) represent structural categories and do not hold individual column types; leaf nodes (`is_folder = False`, `len(children) == 0`) hold specific Excel data types.
  - State Integrity: Editing an element's data type marks `isDirty = true`, seamlessly integrating with 1-click template auto-synchronization and dirty state interception.
- **Principle III (Composite Pattern & Dynamic Polymorphism)**: When child nodes are deleted or moved away and a folder's child list becomes empty, the node dynamically transitions to a leaf node (`is_folder = False`), automatically activating its data type state, displaying its type badge, and qualifying for Excel Row 1 column export.
- **Principle IV (Library-First & TDD)**: Unit tests for Excel type inference, model encapsulation, dynamic state transitions, and export formatting in domain adapters (`test_excel_adapter.py`, `test_composite.py`) and RPC integration tests (`test_eel_bridge.py`) are specified upfront.
- **Principle V (Self-Contained Excel Processing)**: Leverages `openpyxl` number formats and cell types without COM dependencies or MS Excel installation requirements.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) audited across models, adapters, RPC endpoints, and UI views.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates clean-slate creation, empty Excel columns, mixed type detection fallbacks, child deletion leading to folder $\rightarrow$ leaf conversion, and catalog drag-and-drop type inheritance.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Viewing Leaf Element Data Types in Canvas & Excel Auto-Detection (Priority: P1) 🎯 MVP

As a database architect or financial analyst, I want the Hierarchy Constructor Workspace to automatically detect and display the Excel data type for each non-folder (leaf) element (e.g. Text, Integer, Decimal, Currency, Percentage, Date, Time, DateTime, Boolean) via a distinct badge in the canvas tree, so that I have immediate visibility into the underlying data types of all database columns.

**Why this priority**: Core viewing capability and foundation for Excel type synchronization across the application.

**Independent Test**:
1. Import an Excel file with multiple columns having diverse data formats (e.g., `EmployeeName` as Text, `Salary` as Currency, `HireDate` as Date, `IsActive` as Boolean).
2. Verify that in the Hierarchy Constructor Workspace canvas:
   - Leaf node `EmployeeName` displays a `[Text]` badge.
   - Leaf node `Salary` displays a `[Currency]` badge.
   - Leaf node `HireDate` displays a `[Date]` badge.
   - Leaf node `IsActive` displays a `[Boolean]` badge.
   - Folder nodes (e.g., category parent nodes) do NOT display a data type badge.
3. Verify that creating a leaf node manually from scratch or adding an unformatted header defaults cleanly to `[Text]`.

**Acceptance Scenarios**:

1. **Given** an Excel file with formatted data columns, **When** imported via `import_excel_file`, **Then** the backend inspects column formats and sample cell values to infer each column's standard Excel type and assigns it to the corresponding leaf `HierarchyNode`.
2. **Given** a rendered hierarchy tree in the workspace canvas, **When** examining leaf nodes (`children.length === 0`), **Then** each leaf element renders a styled data type badge (e.g., `.node-type-badge`) showing its current type.
3. **Given** a folder node (`children.length > 0`), **When** rendered in the canvas, **Then** no data type badge is displayed.
4. **Given** a column with no data rows or ambiguous formats, **When** imported, **Then** the type defaults to `Text`.

---

### User Story 2 - Editing Leaf Element Data Type via Modal Dialog (Priority: P1)

As a user restructuring a database schema, I want to edit the data type of any leaf element by selecting from a list of standard Excel types in the edit modal dialog, so that I can re-type columns (e.g., convert a raw string column to `Date` or `Currency`) before generating templates.

**Why this priority**: Core editing functionality empowering users to define and customize schema column types.

**Independent Test**:
1. Select a leaf element (e.g., `TransactionAmount`) currently typed as `Text`.
2. Click the edit pencil button (`.rename-node`) or double-click the node.
3. In the edit modal, observe the "Element Data Type" dropdown pre-selected with `Text`.
4. Change the dropdown selection to `Currency` and click "Save Changes" (or press `Enter`).
5. Verify that the canvas node badge updates immediately to `[Currency]`.
6. Verify that `isDirty` is set to `true`.

**Acceptance Scenarios**:

1. **Given** a leaf node in the canvas, **When** the edit modal is opened, **Then** an "Element Data Type" dropdown (`#selectNodeType`) is visible and pre-populated with the leaf's current data type.
2. **Given** the "Element Data Type" dropdown, **When** clicked, **Then** all standard Excel types are available for selection:
   - `Text` (String)
   - `Integer` (Whole Number)
   - `Decimal` (Floating Point Number)
   - `Currency` (Monetary Amount)
   - `Percentage` (Percent Value)
   - `Date` (Calendar Date)
   - `Time` (Time of Day)
   - `DateTime` (Timestamp)
   - `Boolean` (Logical TRUE/FALSE)
3. **Given** a user changes the data type and saves, **Then** backend RPC updates the node's `data_type`, returns updated roots, updates the UI badge, and sets `isDirty = true`.
4. **Given** a folder node (node with children), **When** its edit modal is opened, **Then** the type selector is hidden or disabled with an informative label explaining that data types apply exclusively to leaf elements.

---

### User Story 3 - Dynamic Folder-to-Leaf Transformation upon Child Deletion or Movement (Priority: P1)

As a user modifying an existing tree hierarchy, when I delete the last child of a folder (or move all its children out), I want the former folder to dynamically transform into a leaf element, display its data type badge, allow type editing, and be included in the Excel Row 1 export paths, so that no orphaned or untyped dead nodes exist.

**Why this priority**: Directly resolves structural edge cases where child removal changes the ontological classification of a node.

**Independent Test**:
1. Create a parent folder `Finance` with a single child leaf `Budget` (type `Currency`).
2. Delete the child node `Budget` using the delete button.
3. Verify that `Finance` dynamically evaluates to a leaf node (`is_folder = False`).
4. Verify that `Finance` immediately displays a `.node-type-badge` (retaining its previous type or defaulting to `Text`).
5. Verify that clicking edit on `Finance` now allows selecting an Element Data Type.
6. Verify that `Export Preview` tab now lists `Finance` as an exported leaf path, and saving to Excel exports `Finance` with its assigned column format.

**Acceptance Scenarios**:

1. **Given** a folder node with exactly 1 child, **When** the child is deleted via `delete_node` or dragged to another location via `move_node`, **Then** the parent node's `is_folder` becomes `False`.
2. **Given** a node that has transformed from a folder to a leaf, **When** rendered in the UI, **Then** it renders a `.node-type-badge`, enables type editing in `#nodeModal`, and appears in `Export Preview`.
3. **Given** a leaf node that is upgraded to a folder by dragging a child into it (`NEST_CHILD`), **When** re-rendered, **Then** its data type badge is hidden and it is treated as a structural catalog.

---

### User Story 4 - Sidebar Catalog Data Type Inheritance during Drag & Drop (Priority: P2)

As a user building a hierarchy by dragging headers from the Excel Header Catalog sidebar, I want new nodes created in the canvas to automatically inherit the column data type detected in the Excel file, so that I don't have to manually re-assign data types for every imported column.

**Why this priority**: Eliminates redundant user effort and ensures data type fidelity when constructing hierarchies from catalog items.

**Independent Test**:
1. Import an Excel file where column `HireDate` is formatted as `Date` and `Salary` is formatted as `Currency`.
2. Drag `HireDate` from the Header Catalog sidebar into the Hierarchy Constructor Workspace canvas.
3. Verify the newly created canvas node has `data_type: "Date"` and displays the `[Date]` badge.
4. Drag `Salary` from the catalog into the canvas.
5. Verify the newly created canvas node has `data_type: "Currency"` and displays the `[Currency]` badge.

**Acceptance Scenarios**:

1. **Given** imported Excel headers with inferred column types, **When** cached in the frontend session, **Then** each catalog item retains its detected `data_type`.
2. **Given** a catalog item dragged and dropped onto the canvas, **When** `handleAddHeaderNode` calls `add_node`, **Then** the node is created with the catalog item's detected `data_type` (falling back to `Text` if none).

---

### User Story 5 - Persisting Updated Data Types into Excel Template upon Saving (Priority: P2)

As a user exporting a finalized hierarchy, I want all assigned element data types to be written directly into the exported Excel workbook / template (`.xlsx`) using standard openpyxl number formats and column formatting, so that when the template is opened in Microsoft Excel or imported into downstream systems, each column has its exact expected Excel data type and number format.

**Why this priority**: Guarantees end-to-end data fidelity and fulfills the round-trip Excel type synchronization contract.

**Independent Test**:
1. Re-type leaf nodes in the workspace (e.g. `Revenue` -> `Currency`, `CreatedDate` -> `Date`, `Quantity` -> `Integer`, `Discount` -> `Percentage`).
2. Export the template workbook via "Export Excel" or 1-click template sync (`save_template_sync`).
3. Inspect the exported `.xlsx` workbook with openpyxl / Excel.
4. Verify that Row 1 headers match the leaf paths AND the corresponding columns (Row 1 cell & column number formatting) have:
   - `Revenue`: Currency format (e.g., `FORMAT_CURRENCY_USD_SIMPLE` or `"$#,##0.00"`)
   - `CreatedDate`: Date format (e.g., `FORMAT_DATE_YYYYMMDD2` or `"yyyy-mm-dd"`)
   - `Quantity`: Integer format (`"0"` / `"#,##0"`)
   - `Discount`: Percentage format (`"0.00%"`)

**Acceptance Scenarios**:

1. **Given** a hierarchy with custom leaf data types, **When** `export_multi_sheet_template` or `export_reorganized_row1` is executed, **Then** openpyxl applies the standard Excel number format (`cell.number_format`) matching each leaf's assigned `data_type`.
2. **Given** a multi-sheet session, **When** `save_template_sync` exports all sheets, **Then** each sheet preserves the specific column data types configured in its respective workspace forest.
3. **Given** an exported template is re-imported into the application, **Then** the assigned data types are accurately recognized and displayed on the leaf badges.

---

### User Story 6 - Export Preview Tab Data Type Visibility (Priority: P3)

As a user reviewing the planned export in the "Export Preview" sidebar tab, I want each leaf path card to display both the full backslash path and its target Excel data type badge, so that I can audit the entire schema before writing to disk.

**Why this priority**: Provides complete pre-export auditability and clarity.

**Independent Test**:
1. Open the "Export Preview" tab in the unified sidebar.
2. Verify each path card displays the leaf path (e.g., `Finance\Q1\Revenue`) and an associated type pill badge (e.g., `[Currency]`).

---

## Edge Cases

- **Child Deletion / Evacuation**: Deleting the only child of a container converts it instantly into a leaf with a valid data type (`Text` or restored prior type), recalculates all leaf paths, updates the Export Preview, and marks `isDirty = true`.
- **Mixed-Type Data Columns in Excel**: When inferring types from existing Excel data rows (Rows 2..100), if a column contains mixed types (e.g. some numbers and some text), the inference engine selects the majority type or safely falls back to `Text`.
- **Empty Sheets / Header-Only Sheets**: When an Excel sheet contains only Row 1 headers without data rows, column number formatting in Excel is checked first; if unformatted, it defaults cleanly to `Text`.
- **Exotic / Custom Number Formats**: Formats like accounting brackets `($#,##0)` or regional date formats `DD.MM.YYYY` are categorized into standard buckets (`Currency`, `Date`, etc.).
- **Renaming vs Type Editing**: A user can edit the node name, data type, or both simultaneously in the modal without conflicting mutations.
- **Zero-Data Workspace**: Starting from scratch with an empty canvas allows creating root and child leaf nodes with selectable data types without requiring an initial Excel file.
- **Whitespace & Case Insensitivity in Type Strings**: Internal type serialization uses normalized canonical identifiers (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `HierarchyNode` in `src/hierarchy_lib/models/node.py` MUST store a `data_type: Optional[str] = "Text"` attribute for leaf nodes.
- **FR-002**: `HierarchyNode.to_dict()` MUST include `"data_type": self.data_type` in its serialized dictionary.
- **FR-003**: `HierarchyNode` MUST provide a `set_data_type(data_type: str)` method with validation against the canonical Excel standard type list.
- **FR-004**: The system MUST support the following 9 canonical Excel standard data types:
  1. `Text` (`@`)
  2. `Integer` (`0`)
  3. `Decimal` (`0.00`)
  4. `Currency` (`"$"#,##0.00`)
  5. `Percentage` (`0.00%`)
  6. `Date` (`yyyy-mm-dd`)
  7. `Time` (`hh:mm:ss`)
  8. `DateTime` (`yyyy-mm-dd hh:mm:ss`)
  9. `Boolean` (`General`)
- **FR-005**: `ExcelHierarchyAdapter` in `src/hierarchy_lib/adapters/excel_adapter.py` MUST provide column type inference by inspecting Excel cell data types (`cell.data_type`) and number formats (`cell.number_format`) across sample rows (Rows 2..100).
- **FR-006**: When an Excel file is imported via `import_excel_file`, the header metadata returned MUST include each column's detected data type (e.g. `all_headers_meta: { Sheet1: [ { name: "...", type: "..." } ] }`).
- **FR-007**: Dragging an item from the Header Catalog sidebar into the workspace canvas MUST create a leaf node with the catalog item's detected `data_type`.
- **FR-008**: When a folder's children are deleted or moved such that `len(children) == 0`, the node MUST dynamically evaluate as a leaf (`is_folder = False`), adopt a valid `data_type`, render its type badge, and be included in leaf path calculations and export.
- **FR-009**: `ExcelHierarchyAdapter.export_multi_sheet_template` MUST accept leaf paths along with their `data_type` and apply the corresponding Excel `number_format` and cell formatting for each leaf column.
- **FR-010**: `eel_bridge.py` MUST expose `@eel.expose def update_node(node_id: str, name: Optional[str] = None, data_type: Optional[str] = None) -> Dict[str, Any]` (or dedicated `update_node_type`) to update node attributes.
- **FR-011**: `TreeRenderer` in `src/web/js/tree_renderer.js` MUST render a `.node-type-badge` on every leaf node (`isFolder === false`) and in the `Export Preview` tab path cards.
- **FR-012**: `#nodeModal` in `src/web/index.html` MUST include an "Element Data Type" dropdown (`#selectNodeType`) containing all 9 standard Excel types.
- **FR-013**: `App.openEditModal` in `src/web/js/app.js` MUST populate and pre-select `#selectNodeType` when editing a leaf node, and hide/disable it when editing a folder node.
- **FR-014**: Global system map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document the new `data_type` domain attributes, Excel format mappings, RPC endpoints, and UI badge elements.
- **FR-015**: Comprehensive unit tests (`tests/unit/test_composite.py`, `tests/unit/test_excel_adapter.py`, `tests/unit/test_forest_zone_addition.py`) and integration tests (`tests/integration/test_eel_bridge.py`) MUST verify Excel type detection, leaf badge serialization, folder $\leftrightarrow$ leaf transitions, modal type mutations, and openpyxl format persistence.

### Key Entities

- **`ExcelDataType`**: Canonical enumerated type set (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`) mapped to openpyxl number format strings (`@`, `0`, `0.00`, `"$"#,##0.00`, `0.00%`, `yyyy-mm-dd`, `hh:mm:ss`, `yyyy-mm-dd hh:mm:ss`, `General`).
- **`HierarchyNode.data_type`**: Attribute on `HierarchyNode` representing the Excel column data type for leaf nodes (`None` or inactive for folder nodes).
- **`.node-type-badge`**: UI element rendered alongside `.node-title` in leaf cards and in `Export Preview` path cards showing the active data type with dedicated CSS coloring.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of non-folder (leaf) elements display their assigned Excel data type badge in the Hierarchy Constructor Workspace canvas and Export Preview tab.
- **SC-002**: 100% of imported Excel columns with standard Excel formatting are correctly auto-detected upon import and inherited during sidebar drag-and-drop.
- **SC-003**: 100% of folder nodes whose children are removed immediately transition to valid, typed leaf nodes with zero deadlocks or rendering glitches.
- **SC-004**: Users can view and edit any leaf element data type in <= 2 clicks.
- **SC-005**: 100% of exported template workbooks apply correct Excel `number_format` strings to corresponding columns.
- **SC-006**: 100% automated test suite pass rate across unit and integration tests (`python -m pytest`).

---

## Assumptions

- Folder nodes represent structural grouping hierarchies (categories, schemas, prefixes) and do not directly map to single data values or Excel column formats; only leaf nodes map directly to Excel data columns.
- Standard Excel formatting relies on openpyxl's built-in format constants and standard format strings, requiring zero third-party software or MS Excel installation.
