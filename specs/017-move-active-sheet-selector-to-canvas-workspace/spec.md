# Feature Specification: Move Active Workspace Sheet Selector to Canvas Workspace

**Feature Branch**: `017-move-active-sheet-selector-to-canvas-workspace`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "Move the Active Workspace Sheet to the Hierarchy Constructor Workspace"

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean State Architecture)**:
  - Clean Separation of Concerns:
    - **Hierarchy Constructor Workspace (Left Canvas)**: Houses the interactive **Active Workspace Sheet** selector directly within its header toolbar, giving users immediate visual context and direct control over which worksheet hierarchy is being constructed.
    - **Unified Sidebar (Right Panel)**: Focuses purely on header catalog discovery (`Browse Headers From:` with `[All Sheets / Sheet1 / Sheet2]`, search filter, and leaf path export preview), eliminating redundant sheet selectors in the sidebar.
  - State Integrity: Retains all `isDirty` protection, `#unsavedModal` interceptors, and 1-click template auto-synchronization (`save_template_sync`).
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates UI layout across various screen widths, dropdown change handling, empty states, and dirty-state confirmation workflows.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Direct Active Sheet Switching on Workspace Canvas (Priority: P1) 🎯 MVP

As a user constructing hierarchical trees for specific worksheets, I want the **Active Workspace Sheet** selector to be compactly integrated into the **Hierarchy Constructor Workspace** panel header directly adjacent to the node count badge (`Sheet: [Sales v]`), so that I immediately see and control which sheet I am editing without wasting vertical canvas space.

**Why this priority**: Eliminates visual clutter in the sidebar, saves vertical screen space, and places active canvas control directly where the user is looking and working.

**Independent Test**:
1. Import a multi-sheet Excel file with `Sales` and `Inventory`.
2. Inspect the **Hierarchy Constructor Workspace** panel header on the left canvas.
3. Verify that a compact inline dropdown labeled **Sheet: [Sales v]** is situated in the canvas header title group (adjacent to `#nodeCountBadge` and expand/collapse controls).
4. Change the dropdown from `Sales` to `Inventory`.
5. Verify the canvas seamlessly loads the `Inventory` hierarchy tree.

**Acceptance Scenarios**:

1. **Given** an open workbook with multiple sheets, **When** looking at the Hierarchy Constructor Workspace panel header, **Then** the compact inline Active Sheet dropdown selector is clearly visible alongside the title and node counter.
2. **Given** the Active Sheet selector in the canvas header, **When** the user selects another sheet without unsaved changes, **Then** the canvas updates immediately to that sheet's hierarchy tree.
3. **Given** the Active Sheet selector in the canvas header, **When** the user selects another sheet with unsaved changes (`isDirty == true`), **Then** the Unsaved Changes modal appears with `[Update Template & Switch]`, protecting user data before switching.

---

### User Story 2 - Cleaned & Focused Sidebar Header Catalog (Priority: P2)

As a user searching and dragging headers, I want the Unified Sidebar Tab 1 to only display catalog controls (`Browse Headers From:`, search filter, header cards), so that the sidebar is dedicated to header discovery without duplicating active workspace sheet selection.

**Why this priority**: Simplifies the sidebar UI and eliminates cognitive confusion between the editing target and the catalog source.

**Independent Test**:
1. Open the sidebar Tab 1 (Header Catalog).
2. Verify that there is only one sheet dropdown: **Browse Headers From: [All Sheets (Combined) v]**.
3. Select `All Sheets` or `Inventory` in the catalog dropdown and search for a header.
4. Drag a header onto the canvas workspace.
5. Verify that the canvas retains its active sheet while receiving the dragged header.

**Acceptance Scenarios**:

1. **Given** the sidebar Tab 1, **When** inspected, **Then** the redundant `#activeSheetSelector` is removed from the sidebar, leaving only `#catalogSheetSelector`.
2. **Given** the catalog dropdown in the sidebar, **When** changed, **Then** it filters catalog headers without affecting the active workspace sheet selection on the canvas.

---

## Edge Cases

- **Small Workspace Widths**: The active sheet selector in the canvas header must be compact (using flexbox with `max-width` and truncation) to prevent overflowing when the sidebar is expanded.
- **Empty / Initial State**: Before any file is imported, the active sheet selector in the canvas header displays a disabled placeholder `(No Sheet Loaded)`.
- **Keyboard Navigation**: The dropdown selector must be fully accessible via Tab and Arrow keys.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Active Workspace Sheet dropdown selector (`#activeSheetSelector`) MUST be located within the **Hierarchy Constructor Workspace** panel header (`.tree-panel .panel-header`).
- **FR-002**: The static `#activeSheetBadge` in the canvas header MUST be replaced with/integrated into the interactive `#activeSheetSelector` styled as a sleek, compact dropdown badge or inline selector.
- **FR-003**: The Unified Sidebar Tab 1 (`#tabContentCatalog`) MUST remove the Active Workspace Sheet selector and retain only the `#catalogSheetSelector` ("Browse Headers From:"), search input, and header list.
- **FR-004**: All event listeners in `src/web/js/app.js` (`isDirty` tracking, unsaved changes modal interception, sheet switching, and option population) MUST continue to operate without regression.
- **FR-005**: All test suites in `pytest` MUST continue to pass with 100% pass rate (`python -m pytest`).
- **FR-006**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document the new layout organization.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of active sheet switching controls are accessible directly on the workspace canvas header.
- **SC-002**: Sidebar Tab 1 vertical space is reduced by removing redundant controls, allowing more header items to be visible without scrolling.
- **SC-003**: 100% of automated test suites pass with 0 failures (`python -m pytest`).

---

## Assumptions

- Moving `#activeSheetSelector` to the canvas header retains its HTML `id="activeSheetSelector"`, preserving JS references and backward compatibility.
