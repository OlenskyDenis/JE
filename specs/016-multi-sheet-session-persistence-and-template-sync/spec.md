# Feature Specification: Multi-Sheet Session Persistence & Template Auto-Sync

**Feature Branch**: `016-multi-sheet-session-persistence-and-template-sync`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "When editing the Hierarchy Constructor Workspace and selecting a different sheet in the Active Workspace Sheet, the user is prompted to save their work to a file, after which all changes on the sheets should be saved to the system so that when the user returns, they can see their work, and any subsequent edits to other sheets should prompt an update to the existing template and automatically save the changes to the file"

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean State Architecture)**:
  - Multi-Sheet Session Container: Manages per-sheet `WorkspaceForest` instances in memory (`sheet_forests: Dict[str, WorkspaceForest]`), preserving each sheet's hierarchy when switching back and forth.
  - Bound Template File State: Binds `current_template_path` upon initial template save, enabling seamless updates to the existing template file without re-prompting the OS file picker on every subsequent edit.
  - Multi-Sheet Clean Export: `ExcelHierarchyAdapter` exports all modified sheet hierarchies simultaneously to the template workbook (`max_row == 1` across all sheets).
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates multi-sheet workflows across 10+ sheets with arbitrary switching, verifying 0 node loss and consistent template file synchronization.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Sheet Session Hierarchy Persistence (Priority: P1) 🎯 MVP

As a user organizing a complex multi-sheet workbook, I want my custom hierarchy tree on Sheet A (`Sales`) to remain intact in the system when I switch to Sheet B (`Inventory`) and later return to Sheet A, so that I can work across multiple sheets without losing my progress on any sheet.

**Why this priority**: Solves the core limitation where switching sheets discarded previous sheet trees.

**Independent Test**:
1. Import a multi-sheet file with `Sales` and `Inventory`.
2. On `Sales`, add custom child nodes `Sales -> North -> Branch1`.
3. In Active Workspace Sheet, switch to `Inventory`.
4. On `Inventory`, add custom child nodes `Inventory -> Warehouse -> BinA`.
5. Switch Active Workspace Sheet back to `Sales`.
6. Verify `Sales` displays `Sales -> North -> Branch1` with all nodes fully preserved.
7. Switch back to `Inventory` and verify `Inventory -> Warehouse -> BinA` is also preserved.

**Acceptance Scenarios**:

1. **Given** an active session with multiple sheets, **When** the user modifies the hierarchy on Sheet A and switches to Sheet B, **Then** Sheet A's `WorkspaceForest` is retained in memory.
2. **Given** Sheet A's retained hierarchy, **When** the user switches back to Sheet A, **Then** the canvas loads Sheet A's modified hierarchy tree exactly as left.
3. **Given** node mutations on any sheet (adds, moves, deletions), **When** switching sheets, **Then** all sheets maintain their independent tree structures, leaf paths, and collapse states.

---

### User Story 2 - Bound Template File Auto-Sync & Streamlined Update Prompt (Priority: P2)

As a user who has saved/exported a template file (`Шаблон_<name>.xlsx`), I want subsequent edits on other sheets to automatically update this bound template file when saving or switching sheets (with a single-click update confirmation or auto-save), so that I do not have to repeatedly navigate the OS save dialog.

**Why this priority**: Eliminates repetitive file dialog prompts and ensures all multi-sheet changes are continuously synchronized into the target template workbook.

**Independent Test**:
1. On `Sales`, make a change and save to `Шаблон_Data.xlsx` via the native save dialog.
2. The template path `Шаблон_Data.xlsx` is now bound to the session.
3. Switch to `Inventory` and add new nodes.
4. Attempt to switch to `Customers` or click Save:
   - System prompts: *"Update template 'Шаблон_Data.xlsx' with your changes to 'Inventory'?"* with [Update & Switch], [Discard & Switch], [Cancel].
5. Click **Update & Switch**:
   - System writes the latest `Sales` AND `Inventory` reorganized leaf paths into `Шаблон_Data.xlsx` without reopening the OS file picker.
   - Canvas switches to `Customers`.
6. Open `Шаблон_Data.xlsx` and verify Row 1 contains updated paths for both `Sales` and `Inventory` (`max_row == 1`).

**Acceptance Scenarios**:

1. **Given** an initial template save to `output_path`, **When** the save completes, **Then** `current_template_path` is bound to the active session.
2. **Given** a bound `current_template_path` and unsaved changes on the active sheet, **When** the user switches sheets, **Then** the modal offers `[Update Template & Switch]` which immediately updates the bound file without opening the OS file dialog.
3. **Given** a multi-sheet template export, **When** written to disk, **Then** all modified sheets in the session write their custom leaf paths to Row 1, while unmodified sheets retain their streamed Row 1 headers, and all sheets satisfy `max_row == 1`.
4. **Given** the toolbar **Export Excel** button, **When** a template file is bound, **Then** a quick "Save / Sync Template" action is available alongside "Save As / Export As New File".

---

## Edge Cases

- **File Deleted or Moved Externally**: If the bound template file is moved or deleted, the system falls back to opening the native save dialog to select a new destination path.
- **Initial Save Cancelled**: If the user cancels the initial save dialog, no template path is bound, and future prompts continue to prompt for initial save destination.
- **Scratch Sessions**: For sessions created from scratch without an imported file, per-sheet persistence and template binding operate identically.
- **Unmodified Sheets**: Sheets that were never edited continue to export their original Row 1 headers in the template file.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Backend MUST maintain a multi-sheet session container (`sheet_forests: Dict[str, WorkspaceForest]`) tracking the live hierarchy tree for every sheet in the workbook session.
- **FR-002**: Switching active sheets (`switch_active_sheet`) MUST preserve the outgoing sheet's `WorkspaceForest` in `sheet_forests` and load the incoming sheet's `WorkspaceForest` (or initialize it from Row 1 headers if first visit).
- **FR-003**: Backend MUST track `current_template_path: Optional[str]` representing the bound template file for the current session.
- **FR-004**: `export_reorganized_row1` / multi-sheet export MUST write all modified sheet hierarchies in `sheet_forests` to their respective worksheets in Row 1 in a single clean workbook (`max_row == 1`).
- **FR-005**: When `current_template_path` is bound and the user changes the active workspace sheet while `isDirty == true`, the Unsaved Changes modal MUST offer `Update Template & Switch` (directly syncing `current_template_path` without reopening the OS file picker).
- **FR-006**: When no template is bound, `Save & Switch` MUST open the OS save dialog to establish `current_template_path`, then save and switch.
- **FR-007**: Frontend MUST display the bound template file name / status in the UI (e.g. `Template: Шаблон_<name>.xlsx (Synced)`).
- **FR-008**: All test suites in `tests/unit/test_excel_adapter.py` and `tests/integration/test_eel_bridge.py` MUST be updated to verify multi-sheet session persistence, round-trip sheet switching without node loss, and multi-sheet template synchronization.
- **FR-009**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document the multi-sheet session state container and template synchronization lifecycle.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of node modifications across all sheets are preserved when switching between sheets (0% node loss).
- **SC-002**: Updating an existing bound template file requires exactly 1 click without OS file dialog navigation.
- **SC-003**: 100% of sheets in the exported template file contain accurate Row 1 headers with zero data rows (`max_row <= 1`).
- **SC-004**: 100% of automated test suites pass with 0 failures (`python -m pytest`).

---

## Assumptions

- Per-sheet `WorkspaceForest` instances are kept in memory for the duration of the application session.
- Updating an existing template file overwrites the previous template artifact cleanly.
