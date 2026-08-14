# Feature Specification: Preservation of Original Excel Column Sequence in Hierarchy Trees

**Feature Branch**: `012-preserve-excel-column-order`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "When generating the hierarchy structure automatically, the system must strictly preserve the original sequence of columns as they appear in the Excel file from left to right. The Hierarchy Constructor Workspace must NOT sort elements alphabetically at any level of the tree."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: No source code is created, edited, or deleted during this specification phase.
- **Principle II (OOP & SOLID)**: Clean architectural separation of data normalization (trimming, deduplication) from ordering policies, preserving FIFO / chronological sequence across all layers.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) loaded and consulted. Traced `ExcelHierarchyAdapter.read_row1_headers` -> `HeaderService.process_headers` -> `PathParserService.parse_header_paths` -> `eel_bridge.py` -> `tree_renderer.js`.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Verified that removing alphabetical sorting preserves full functionality when no file is loaded, on empty sheets, and for single-column sheets without causing key collisions or deadlocks.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Left-to-Right Excel Column Tree Sequence (Priority: P1) 🎯 MVP

As a database architect importing an existing Excel workbook, I want the auto-generated tree structure in the Hierarchy Constructor Workspace to match the exact left-to-right sequence of columns in the spreadsheet, so that the logical flow and domain structure designed in the Excel sheet are preserved rather than scrambled by alphabetical sorting.

**Why this priority**: Core requirement directly requested by the user.

**Independent Test**: Create an Excel sheet with Row 1 headers `["Zebra\\Stripes", "Alpha\\First", "Beta\\Second"]`, import the sheet, and verify the tree canvas displays root nodes in exact order: `Zebra` first, `Alpha` second, `Beta` third (NOT `Alpha`, `Beta`, `Zebra`).

**Acceptance Scenarios**:

1. **Given** an Excel sheet with headers `["Zebra", "Alpha", "Beta"]`, **When** imported via `import_excel_file`, **Then** the canvas displays root nodes in the order `Zebra`, `Alpha`, `Beta`.
2. **Given** an Excel sheet with nested headers `["Category\\Z_Item", "Category\\A_Item"]`, **When** parsed into `Category`, **Then** the children under `Category` appear in order `Z_Item`, `A_Item`.
3. **Given** any depth of hierarchy, **When** rendered on canvas, **Then** no alphabetical sorting is applied at root, intermediate folder, or leaf levels.

---

### User Story 2 - Stable First-Appearance Deduplication (Priority: P2)

As a user importing sheets with duplicate header values, I want deduplication to maintain the position of the first occurrence of each header, so that column order stability is guaranteed.

**Why this priority**: Ensures duplicate elimination does not shuffle column positions.

**Independent Test**: Pass `["Beta", "Alpha", "Beta", "Gamma"]` to header processing and verify the output is `["Beta", "Alpha", "Gamma"]`.

**Acceptance Scenarios**:

1. **Given** a list of headers with duplicates, **When** processed by `HeaderService`, **Then** duplicate items are removed while the first-seen position of each item is strictly preserved.

---

### User Story 3 - Synchronized Left-to-Right Sequence in Sidebar & Export (Priority: P3)

As a user inspecting the Excel Header Catalog in the sidebar and the Leaf Node Absolute Paths panel, I want all panels to present headers in the original column sequence from left to right, maintaining consistency across the entire GUI.

**Why this priority**: Eliminates visual discrepancy between the canvas, sidebar catalog, and leaf path list.

**Independent Test**: Load an Excel sheet and confirm that the sidebar catalog items and middle panel path cards follow the exact column order of the sheet.

**Acceptance Scenarios**:

1. **Given** an imported sheet, **When** viewing the sidebar catalog and leaf paths list, **Then** all lists reflect the original left-to-right column order without alphabetical reordering.

---

## Edge Cases

- **Unordered Path Segments in Excel**: If an Excel sheet contains `["Store\\Dept\\Cashier", "Store\\Dept\\Manager"]`, `Store` is created first with `Dept`, containing `Cashier` followed by `Manager`.
- **Interspersed Sibling Branches**: If headers are `["Dept\\A", "Other\\X", "Dept\\B"]`, `Dept` is created at Col 1 with child `A`, `Other` is created at Col 2 with child `X`, and when `Dept\B` is encountered at Col 3, `B` is appended as the second child of `Dept`.
- **Case-Insensitive Deduplication**: If headers are `["Alpha", "alpha"]`, the first occurrence (`Alpha`) is preserved and subsequent case-insensitive duplicates are filtered out.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `HeaderService.process_headers` in `src/hierarchy_lib/services/header_service.py` MUST NOT sort headers alphabetically and MUST preserve exact first-seen insertion order (FIFO).
- **FR-002**: `ExcelHierarchyAdapter.read_row1_headers` in `src/hierarchy_lib/adapters/excel_adapter.py` MUST return headers in their exact left-to-right column sequence from Row 1.
- **FR-003**: `PathParserService.parse_header_paths` in `src/hierarchy_lib/services/path_parser.py` MUST construct root nodes and child arrays in the exact chronological encounter order of header paths.
- **FR-004**: `eel_bridge.py` endpoints (`import_excel_file`, `switch_active_sheet`) MUST deliver headers and roots to the frontend in original left-to-right column sequence.
- **FR-005**: All unit tests verifying `HeaderService`, `PathParserService`, and `ExcelHierarchyAdapter` MUST be updated to assert original column sequence preservation instead of alphabetical sorting.
- **FR-006**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to reflect chronological column sequence preservation.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of imported Excel sheets display root nodes, sub-folders, and leaf nodes in exact left-to-right column order.
- **SC-002**: Zero alphabetical sorting calls (`.sort()`) executed during header processing, path parsing, or canvas rendering.
- **SC-003**: 100% of unit and integration tests pass with 0 regressions (`python -m pytest`).

---

## Assumptions

- Search filtering in the sidebar (`sidebarSearch`) continues to filter in real-time matching substring queries while preserving the relative sequence of matching items.
