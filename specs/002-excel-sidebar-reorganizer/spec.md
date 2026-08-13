# Feature Specification: Excel Header Reorganization & Database Structure Designer

**Feature Branch**: `feature/excel-sidebar-reorganizer`  
**Created**: 2026-08-13  
**Status**: Draft  

**Input**: User description: "Build an Excel header reorganization and database structure designer. Key features: 1) Import logic: read data exclusively from the first row (headers) of the selected sheet using openpyxl. 2) Sheet management: Add a UI control to switch between sheets of the imported file, updating available headers accordingly. 3) Sidebar UI: Extract and display all unique header elements alphabetically with real-time search/filtering. 4) Non-destructive Drag-and-Drop: Allow dragging headers from the sidebar into the main tree constructor on the left. The dragged element must remain in the sidebar so it can be reused. 5) Export logic: Write the reconstructed tree elements sequentially into the first row (horizontally, across columns) of the corresponding sheet (retaining the original sheet name)."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is generated during this specification phase.
- **OOP & SOLID Design**: Header management and sheet processing follow modular SOLID principles.
- **Library-First & TDD**: Excel header extraction, deduplication, and horizontal row export are defined as standalone core library features with TDD.
- **Self-Contained Excel**: Processing relies on `openpyxl` without requiring Microsoft Excel app installation.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Sheet Header Extraction & Sidebar View (Priority: P1)

As a database designer or data analyst, I want to import an Excel file, select any sheet, and view all unique headers from Row 1 sorted alphabetically in a sidebar with live search, so that I can quickly explore available data fields.

**Why this priority**: Core value of the feature relies on reading header data from any sheet and giving the user a searchable catalog of available headers.

**Independent Test**: Can be tested by importing an `.xlsx` file with multiple sheets, switching between sheets, and verifying the sidebar displays deduplicated, sorted headers matching Row 1 of the selected sheet with real-time search filtering working.

**Acceptance Scenarios**:

1. **Given** an imported `.xlsx` file with multiple sheets ("Sales", "Inventory"), **When** the file is opened, **Then** the sheet selector UI populates with all sheet names and selects the first sheet by default.
2. **Given** an active sheet with headers in Row 1, **When** headers are extracted, **Then** all unique non-empty header strings are displayed in the sidebar in alphabetical order.
3. **Given** a populated sidebar list, **When** the user types a term into the sidebar search input, **Then** the list filters instantly in real-time to show only matching header items.
4. **Given** an active sheet selection, **When** the user switches to a different sheet in the dropdown, **Then** the sidebar immediately clears and populates with the unique headers from Row 1 of the newly selected sheet.

---

### User Story 2 - Non-Destructive Drag-and-Drop Header Tree Construction (Priority: P2)

As a database architect, I want to drag header elements from the sidebar into the main tree builder without removing them from the sidebar, so that I can reuse identical header names in multiple branches of my database structure.

**Why this priority**: Enables structural modeling and reorganization of tree hierarchies while retaining full availability of source headers.

**Independent Test**: Can be tested by dragging a header item from the sidebar into the tree constructor. The dropped item creates a node in the tree, while the source item remains intact in the sidebar for subsequent drags.

**Acceptance Scenarios**:

1. **Given** a sidebar containing header items, **When** the user drags a header into the main tree canvas or onto a parent node, **Then** a new tree node labeled with that header is created.
2. **Given** a header dragged and dropped into the tree builder, **When** checking the sidebar, **Then** the original header item remains visible and usable in the sidebar.
3. **Given** existing nodes in the tree constructor, **When** new headers are dropped as children or siblings, **Then** the tree updates its internal composite structure correctly.

---

### User Story 3 - Horizontal Row-1 Excel Export by Sheet (Priority: P3)

As a data manager, I want to export my reconstructed tree structure back into the Excel file, writing the elements sequentially into Row 1 across columns of the corresponding sheet while keeping the original sheet name.

**Why this priority**: Completes the round-trip workflow, persisting the reorganized structure back into Excel format.

**Independent Test**: Can be tested by building a tree, triggering export, and inspecting the generated `.xlsx` file to confirm that Row 1 contains the ordered tree element labels across columns A, B, C... under the original sheet name.

**Acceptance Scenarios**:

1. **Given** a reconstructed tree structure for an active sheet, **When** the user exports the project to Excel, **Then** the system writes the ordered tree node labels sequentially into Row 1 (horizontally across columns A, B, C...) of that sheet.
2. **Given** a multi-sheet workbook, **When** exporting, **Then** the original sheet name is preserved, and other unedited sheets remain untouched.

---

### Edge Cases

- **Empty Row 1**: If Row 1 of a selected sheet contains no text or only whitespace, the sidebar displays a clear notice: "No headers found in Row 1 of this sheet."
- **Duplicate Headers in Row 1**: Duplicate header strings in Row 1 are deduplicated so each unique header appears once in the sidebar list.
- **Special Characters / Whitespace**: Leading and trailing whitespace in cell values are trimmed for sidebar display and node labels.
- **Locked Export File**: If the target export file is open in another application and write-locked, the system notifies the user to close the file or select a different path.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read header data exclusively from the first row (Row 1) of a selected sheet in an imported `.xlsx` file using `openpyxl`.
- **FR-002**: System MUST provide a sheet management UI control allowing users to select and switch between all sheets in the imported workbook.
- **FR-003**: System MUST extract, deduplicate, and display all unique non-empty headers from Row 1 of the selected sheet alphabetically in a sidebar.
- **FR-004**: System MUST provide a real-time text input in the sidebar to filter the displayed headers dynamically as the user types.
- **FR-005**: System MUST support non-destructive drag-and-drop, allowing headers to be dragged from the sidebar into the main tree constructor while keeping the dragged item in the sidebar for reuse.
- **FR-006**: System MUST write the reconstructed tree nodes sequentially into Row 1 (horizontally across columns A, B, C...) of the corresponding sheet upon export, preserving the original sheet name.

### Key Entities

- **Workbook Sheet Session**: Represents an imported Excel workbook session, tracking sheet names, active sheet index, and Row 1 header lists per sheet.
- **Sidebar Header Item**: Represents a unique, draggable header string extracted from Row 1 of the active sheet.
- **Tree Constructor Node**: Represents a node within the hierarchy canvas created by dragging a header item or adding custom nodes.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sheet switching updates the active sheet and sidebar header list in under 500 milliseconds.
- **SC-002**: Sidebar header extraction, deduplication, and alphabetical sorting for up to 1,000 cells complete in under 300 milliseconds.
- **SC-003**: Real-time sidebar search filtering updates the visible header list in under 100 milliseconds per keystroke.
- **SC-004**: 100% of exported files write tree elements accurately into Row 1 across columns without modifying non-target rows or unedited sheets.

---

## Assumptions

- Excel files are provided in standard `.xlsx` format.
- Microsoft Excel software installation is NOT required on host system (uses `openpyxl`).
- Web UI runs locally in an Eel application window matching existing project setup.
