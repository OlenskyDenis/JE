# Feature Specification: Intuitive Sheet Management, Unsaved Changes Protection & Cross-Sheet Header Catalog

**Feature Branch**: `015-sheet-manager-save-prompt-and-cross-sheet-catalog`  
**Created**: 2026-08-14  
**Status**: Draft (Clarified with First-Time User Experience Architecture)  

**Input**: User directive: "When a user selects a different sheet in the Sheet Manager, prompt to save changes. Make the interface completely intuitive for a first-time user: separate Active Workspace Sheet editing from Cross-Sheet Header Catalog browsing, display an Active Sheet badge on the canvas, and clearly label Leaf Paths as Export Preview (Row 1)."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean UI State Decoupling)**: Clean separation of concerns:
  1. `Active Workspace Sheet State`: Owns canvas `WorkspaceForest`, modified/dirty tracking, and sheet switch confirmation.
  2. `Catalog Header Source State`: Reads and streams Row 1 headers from any selected sheet (or all sheets) without altering or resetting the canvas tree.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted. Preserves all existing Eel RPC endpoints, DOM selectors, and Drag & Drop mechanics.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validated for first-time user journeys: zero-data states, single-sheet workbooks, multi-sheet cross-catalog browsing, canceling save prompts, and dragging cross-sheet items into nested canvas folders.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Unsaved Changes Protection on Active Sheet Switch (Priority: P1) 🎯 MVP

As a user who has modified the tree structure on the active sheet, I want to be prompted with a clear confirmation dialog whenever I change the active workspace sheet, so that my work is never accidentally overwritten or lost.

**Why this priority**: Eliminates the risk of catastrophic data loss during sheet navigation.

**Independent Test**:
1. Import a multi-sheet Excel file (`Sales` and `Inventory`).
2. Add a new child node to the canvas under `Sales`.
3. Change the active workspace sheet to `Inventory`.
4. Verify an Unsaved Changes modal appears with:
   - **Save & Switch**: Opens native save dialog (`Шаблон_<file>.xlsx`), then switches to `Inventory`.
   - **Discard & Switch**: Clears changes on `Sales` and immediately loads `Inventory`.
   - **Cancel**: Closes modal, keeps workspace on `Sales`, and resets dropdown to `Sales`.

**Acceptance Scenarios**:

1. **Given** a modified (dirty) tree on sheet `Sales`, **When** the user selects `Inventory` in the Active Workspace Sheet selector, **Then** the switch is intercepted and the Unsaved Changes confirmation modal is shown.
2. **Given** the modal is shown, **When** the user clicks [Cancel], **Then** the canvas remains on `Sales` with all nodes intact and the selector reverts to `Sales`.
3. **Given** the modal is shown, **When** the user clicks [Discard & Switch], **Then** dirty state is cleared and the canvas loads `Inventory`.
4. **Given** the modal is shown, **When** the user clicks [Save & Switch], **Then** the save dialog opens; after saving, the canvas loads `Inventory`.
5. **Given** an unmodified (clean) workspace tree, **When** the user switches sheets, **Then** switching occurs immediately without prompting.

---

### User Story 2 - Cross-Sheet Header Catalog Browsing without Canvas Reset (Priority: P2)

As a first-time user constructing a database hierarchy, I want to browse and drag headers from ANY sheet in the workbook (e.g. `Reference` or `Inventory`) into my currently active hierarchy workspace (`Sales`) without resetting or reloading the workspace canvas, so that I can reuse headers across sheets effortlessly.

**Why this priority**: Solves the primary cognitive ambiguity where changing the sheet selector in previous versions wiped out the user's canvas.

**Independent Test**:
1. With `Sales` as the active editing sheet in the workspace, select `Inventory` in the "Browse Headers From" selector (or select "All Sheets").
2. Confirm the sidebar header catalog immediately displays headers from `Inventory`.
3. Confirm the Hierarchy Constructor Workspace canvas remains on `Sales` without reloading or losing existing nodes.
4. Drag a header from `Inventory` into the `Sales` tree canvas.
5. Confirm the node is added to `Sales` hierarchy, and `Sales` is marked as dirty.

**Acceptance Scenarios**:

1. **Given** an active workspace on sheet `Sales`, **When** the user selects `Inventory` in "Browse Headers From", **Then** the sidebar displays headers from `Inventory` while the canvas tree remains on `Sales`.
2. **Given** headers displayed from any sheet, **When** dragging an item into the canvas, **Then** a node is inserted into the active workspace tree without switching the workspace sheet.
3. **Given** the "Browse Headers From" dropdown, **When** opened, **Then** it offers all individual sheet names plus an option `All Sheets (Combined)` allowing universal header access.

---

### User Story 3 - First-Time User Visual Hierarchy & Intuitive Labels (Priority: P3)

As a first-time user, I want clear visual anchors showing which sheet is currently being edited on the canvas and what each sidebar tab does, so that the purpose of every control is immediately self-evident.

**Why this priority**: Eliminates cognitive friction and ensures maximum usability.

**Independent Test**:
1. Open the application with a multi-sheet file loaded.
2. Verify the workspace canvas header displays: `Hierarchy Constructor Workspace` and a prominent badge `Active Sheet: [Sales]`.
3. Verify the sidebar controls clearly distinguish between:
   - **Active Workspace Sheet** (with helper text: *"Editing this sheet's hierarchy"*).
   - **Browse Headers From** (with helper text: *"Select source for draggable headers"*).
4. Verify the second tab is titled `Export Preview (Row 1 Paths)` with the path count badge.

**Acceptance Scenarios**:

1. **Given** an imported session, **When** looking at the workspace header, **Then** an explicit `#activeSheetBadge` displays `Active Sheet: <sheetName>`.
2. **Given** the sidebar tabs, **When** viewed, **Then** Tab 1 is labeled `Header Catalog` and Tab 2 is labeled `Export Preview (Row 1)` with a descriptive tooltip explaining that it previews the Row 1 export output.

---

## Edge Cases

- **User Cancels Native Save Dialog**: If the user selects [Save & Switch] but cancels the OS file dialog, the switch is aborted and the workspace remains on the dirty sheet.
- **Single-Sheet Workbooks**: In single-sheet files, sheet selectors display the single sheet name and dirty tracking functions normally.
- **Scratch Sessions**: When no file is imported, the active sheet is labeled `Active Sheet: Scratch Session (Sheet1)` and "Browse Headers From" remains disabled until a file is imported.
- **Header Source "All Sheets"**: When `All Sheets` is selected in the catalog source, headers from all sheets are presented with small sheet badges indicating their source sheet (e.g. `Region [Sales]`, `Stock_ID [Inventory]`).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST maintain an `isDirty: boolean` flag tracking unsaved modifications in the active workspace tree (set to `true` on node add, move, or delete; reset to `false` on initial load, sheet switch discard, or export).
- **FR-002**: Attempting to switch the active workspace sheet while `isDirty == true` MUST trigger a confirmation modal with options: `Save & Switch`, `Discard & Switch`, and `Cancel`.
- **FR-003**: The workspace header MUST display a dedicated badge element (`#activeSheetBadge`) indicating the currently active editing sheet.
- **FR-004**: The sidebar controls MUST separate workspace sheet switching from header catalog browsing:
  - Control 1: **Active Workspace Sheet** (`#activeSheetSelector`) — switches the tree loaded in the canvas (with dirty state protection).
  - Control 2: **Browse Headers From** (`#catalogSheetSelector`) — controls which sheet's headers are displayed in the draggable catalog without touching the canvas.
- **FR-005**: Selecting a different sheet in `#catalogSheetSelector` MUST dynamically stream and display Row 1 headers from that sheet without reloading or clearing the workspace canvas tree.
- **FR-006**: Dragging headers from `#sidebarHeaderList` into `#treeView` MUST add nodes to the currently active workspace tree regardless of which sheet the headers were sourced from.
- **FR-007**: The sidebar Tab 2 button MUST be labeled `Export Preview` with subtitle/tooltip `Row 1 Output Preview`.
- **FR-008**: All unit and integration test suites MUST be updated to verify dirty state interceptors, cross-sheet header streaming, and visual label fidelity.
- **FR-009**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document dirty state management and dual-mode sheet selectors.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0% accidental data loss when switching sheets; 100% of dirty state switch attempts trigger confirmation.
- **SC-002**: 100% of headers across all workbook sheets can be dragged into the active workspace tree without resetting the canvas.
- **SC-003**: 100% of first-time user test journeys complete tree construction without sheet-switching confusion.
- **SC-004**: 100% of automated test suites pass cleanly (`python -m pytest`).

---

## Assumptions

- Cross-sheet header fetching uses existing `ExcelHierarchyAdapter.read_row1_headers(current_file_path, target_sheet)` streaming.
- Save & Switch uses existing `handleExportReorganizedRow1` export workflow.
