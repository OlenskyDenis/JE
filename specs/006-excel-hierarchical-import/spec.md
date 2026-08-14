# Feature Specification: Automatic Hierarchical Excel Header Import & Workspace Tree Generator

**Feature Branch**: `006-excel-hierarchical-import`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User description: "Rework Excel import behavior: When loading an Excel sheet, automatically parse the header values as hierarchical paths and generate the default tree structure directly in the Hierarchy Constructor Workspace. The path separator is '\\'. For any header containing '\\', the rightmost value must be treated as the final leaf node, and all preceding values must be parsed as nested folders (e.g., 'Root\\Folder\\Leaf' must automatically construct Root -> Folder -> Leaf in the workspace canvas)."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is generated during this specification phase.
- **OOP & SOLID Design**: Parsing and forest generation follow the Single Responsibility and Open/Closed principles, decoupled into core domain services.
- **Library-First & TDD**: Path-to-tree conversion and Excel row 1 parsing logic are defined as testable core domain methods with comprehensive unit and integration test suites.
- **Self-Contained Excel**: Processing relies entirely on `openpyxl` without requiring external spreadsheet software installations.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic Hierarchical Tree Generation on Excel Import (Priority: P1)

As a database architect or data analyst, I want the system to automatically parse Row 1 headers with backslash delimiters (`\`) into a nested composite tree and populate the Hierarchy Constructor Workspace immediately upon loading an Excel sheet, so that I don't have to manually build the folder structure from scratch.

**Why this priority**: Core value of the feature. Automates the conversion of structured path headers into an interactive canvas hierarchy upon loading.

**Independent Test**: Can be tested by importing an Excel file containing headers like `Root\Folder\Leaf1`, `Root\Folder\Leaf2`, and `Root\Other\Leaf3` in Row 1, and verifying that the workspace canvas immediately renders a single root `Root` containing two folders `Folder` and `Other`, with their respective leaves `Leaf1`, `Leaf2`, and `Leaf3`.

**Acceptance Scenarios**:

1. **Given** an Excel file where Row 1 contains `Company\HR\Employees` and `Company\Finance\Payroll`, **When** the file is imported, **Then** the workspace canvas automatically generates:
   - Root folder: `Company`
     - Subfolder: `HR`
       - Leaf: `Employees`
     - Subfolder: `Finance`
       - Leaf: `Payroll`
2. **Given** an Excel header with no backslash delimiters (e.g., `Timestamp`), **When** imported, **Then** the system creates a top-level root node named `Timestamp`.
3. **Given** multiple headers sharing identical parent prefixes (e.g., `Schema\Table\Col1`, `Schema\Table\Col2`), **When** parsed, **Then** common folder nodes are reused and merged rather than duplicated.
4. **Given** an Excel sheet loaded into the workspace, **When** tree generation completes, **Then** the node count badge, canvas tree view, and live path inspector update in real-time.

---

### User Story 2 - Dynamic Tree Rebuilding on Sheet Switching (Priority: P2)

As a user working with multi-sheet workbooks, I want switching sheets in the sheet dropdown to automatically re-parse that sheet's Row 1 headers and rebuild the workspace hierarchy tree to match the selected sheet.

**Why this priority**: Ensures multi-sheet workbooks can be explored sheet-by-sheet with each sheet's hierarchy automatically instantiated on demand.

**Independent Test**: Can be tested by importing a workbook with two sheets containing different header sets, switching between them using the dropdown, and verifying the canvas tree updates to reflect the active sheet's hierarchy.

**Acceptance Scenarios**:

1. **Given** a loaded workbook with Sheet1 (`DB1\Table\Field`) and Sheet2 (`DB2\Schema\Column`), **When** the user selects "Sheet2" in the sheet selector dropdown, **Then** the workspace canvas clears the previous tree and constructs `DB2 -> Schema -> Column`.
2. **Given** a sheet with empty Row 1 headers, **When** selected, **Then** the workspace canvas displays an empty tree state with 0 nodes and the sidebar displays the empty headers message.

---

### User Story 3 - Round-Trip Export and Non-Destructive Editing (Priority: P3)

As a data manager, I want the automatically constructed tree to be fully editable (adding, moving, deleting nodes) and exportable back to Row 1 of the Excel sheet with full path fidelity (`Root\Folder\Leaf`).

**Why this priority**: Preserves complete round-trip integrity between Excel import, visual canvas modeling/reorganization, and horizontal Excel export.

**Independent Test**: Can be tested by importing an Excel file, adding or moving a node in the generated tree, exporting the file, and re-importing to confirm the newly exported paths match the modified hierarchy.

**Acceptance Scenarios**:

1. **Given** an automatically generated tree from imported headers, **When** the user drags a node or adds a new child/root node, **Then** the composite tree updates dynamically.
2. **Given** the modified tree, **When** the user clicks "Export Excel", **Then** the system exports all leaf paths as backslash-delimited strings horizontally across Row 1 columns of the active sheet.

---

### Edge Cases

- **Consecutive / Leading / Trailing Delimiters**: Headers like `\Root\\Folder\Leaf\` or `  Root \ Folder \ Leaf  ` must be cleaned and trimmed to yield segments `["Root", "Folder", "Leaf"]`.
- **Empty / Null Header Cells**: Blank columns, `None` values, or whitespace-only cells in Row 1 are ignored during tree construction.
- **Deep Nesting**: Deeply nested paths (e.g., `L1\L2\L3\L4\L5\Leaf`) must construct the complete chain of nested `CompositeNode` containers leading to the terminal `LeafNode`.
- **Duplicate Exact Paths**: If identical header paths appear in Row 1 (e.g., two columns named `Root\Folder\Item`), the system should avoid duplicate duplicate leaf nodes under the same container or handle deduplication gracefully according to header rules.
- **Mixed Depths**: Headers with varying depths (e.g., `Root\Leaf1` and `Root\Sub\Leaf2` and `Standalone`) under the same workbook must coexist without hierarchy collisions.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse Row 1 headers from the active Excel sheet using the backslash delimiter `\` into hierarchical path segments.
- **FR-002**: For any multi-segment header `S_1\S_2\...\S_k` ($k \ge 2$), system MUST create or reuse `CompositeNode` containers for all prefix segments $S_1, \dots, S_{k-1}$ and instantiate a `LeafNode` for the terminal segment $S_k$.
- **FR-003**: For any single-segment header $S_1$ (containing no `\`), system MUST instantiate a root node named $S_1$.
- **FR-004**: System MUST automatically populate the active `WorkspaceForest` with the parsed hierarchical tree upon opening an Excel file.
- **FR-005**: System MUST rebuild the `WorkspaceForest` and update the UI tree canvas when the user switches the active sheet via the sheet dropdown.
- **FR-006**: System MUST maintain the sidebar header catalog populated with unique headers for drag-and-drop interactions alongside the generated workspace tree.
- **FR-007**: System MUST support exporting the workspace tree back to Row 1 of the target sheet as sequential column leaf paths in `Root\Folder\Leaf` format.

### Key Entities

- **Hierarchical Path**: A string composed of segment names separated by `\` (e.g., `Root\Folder\Subfolder\Leaf`).
- **CompositeNode (Folder/Root)**: Container component in the hierarchy capable of holding child nodes.
- **LeafNode (Terminal Leaf)**: Non-container component representing the rightmost segment of a path.
- **WorkspaceForest**: Multi-root container managing the complete set of top-level trees in the active canvas session.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid backslash-separated headers in Row 1 are correctly parsed and rendered into the workspace tree canvas immediately on file/sheet load without manual user actions.
- **SC-002**: Common path prefixes share container nodes with 0 duplicate ancestor folder instances created for identical prefix paths.
- **SC-003**: Sheet switching re-parses and updates the canvas tree in under 200 milliseconds for standard workbooks (< 500 columns).
- **SC-004**: Full round-trip fidelity: Exporting a loaded tree without edits produces identical Row 1 header paths.

---

## Assumptions

- Excel headers are located exclusively in Row 1 of each worksheet.
- The path delimiter for hierarchy is the backslash character `\`.
- All Excel file operations use `.xlsx` format via `openpyxl`.
- The user operates through the Eel desktop GUI application.
