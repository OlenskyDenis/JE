# Feature Specification: Refresh Imported Excel File Session

**Feature Branch**: `022-refresh-imported-excel-session`  
**Created**: 2026-08-14  
**Status**: Draft  
**Input**: User directive: "clicking the btnRefresh button reconnects to the file that was just imported and updates the data in it if there have been any changes. Handle all exceptions."

---

## Clarifications

### Session 2026-08-14
- Q: When clicking Refresh with external file changes, how should the workspace tree hierarchy be updated? → A: Full Session Reload: Reload the Excel file from disk, updating both the sidebar catalog and the workspace hierarchy tree (prompting to save/discard if there are unsaved changes).

---

## Problem Statement & Context

Currently, clicking the `#btnRefresh` toolbar button calls `get_workspace_tree()`, which merely re-renders the current in-memory `forest` without re-reading the imported Excel file on disk. If a user edits column names, reorders headers, adds new sheets, or modifies column formatting externally in Excel, clicking `#btnRefresh` has no effect.

Users need the `#btnRefresh` button to reconnect to the active Excel file on disk, re-parse all sheets and Row-1 column metadata, and update the Hierarchy Constructor Workspace and Sidebar Catalog in real time, with robust handling of all file, lock, and session exceptions.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Refresh Active Excel Session on External File Changes (Priority: P1) 🎯 MVP

As a database hierarchy designer editing Excel workbooks alongside the desktop app, I want to click the `Refresh` toolbar button (`#btnRefresh`) to reconnect to and re-read the currently imported Excel file from disk, so that any new/renamed columns, updated data types, or added/removed sheets immediately update in my workspace without having to manually re-open the file through the file picker dialog.

**Why this priority**: Core user journey that eliminates repetitive file navigation dialogs and guarantees data synchronization between external Excel edits and the application.

**Independent Test**:
1. Import an Excel workbook `Data.xlsx` with Sheet1 (`Name`, `Salary` [Currency]).
2. Externally edit `Data.xlsx` to add a new column `HireDate` formatted as Date (`yyyy-mm-dd`) and rename `Salary` to `BaseSalary`.
3. Click `#btnRefresh`.
4. Verify the tree canvas and sidebar catalog immediately reflect `Name` [Text], `BaseSalary` [Currency], and `HireDate` [Date], and a toast notification confirms successful refresh.

**Acceptance Scenarios**:
1. **Given** an active Excel session with an imported file, **When** `#btnRefresh` is clicked, **Then** the backend reconnects to the file, re-reads Row-1 headers and column formats across all sheets, and updates the workspace and catalog.
2. **Given** an active session with sheet `"Sales"` selected, **When** the file is refreshed and `"Sales"` still exists, **Then** the active sheet selection remains `"Sales"` and its updated tree is rendered.
3. **Given** an active session with sheet `"OldSheet"` selected, **When** the file is refreshed and `"OldSheet"` was removed in the Excel file, **Then** the application gracefully falls back to the first available sheet in the refreshed workbook.

---

### User Story 2 - Comprehensive Exception and Error Handling (Priority: P2)

As a user interacting with files on the local filesystem, I want the refresh action to gracefully handle missing files, locked files (e.g. open in Excel), permission errors, and corrupted files with clear, actionable toast notifications, so that the application never crashes or leaves the UI in a broken state.

**Why this priority**: Robust exception handling is critical for desktop software stability.

**Independent Test**:
- Attempt refresh when no file has been imported: verify informative warning toast.
- Attempt refresh after moving/renaming the file on disk: verify error toast "File not found".
- Attempt refresh when file is locked exclusively: verify error toast explaining file access lock.

**Acceptance Scenarios**:
1. **Given** no Excel file has been imported yet, **When** `#btnRefresh` is clicked, **Then** the application displays a friendly warning toast ("No active Excel session to refresh.") without making unnecessary disk calls or throwing unhandled errors.
2. **Given** an imported file that was subsequently deleted or moved on disk, **When** `#btnRefresh` is clicked, **Then** the application catches `FileNotFoundError` and shows an error toast ("Cannot refresh: File '<filename>' not found on disk.").
3. **Given** an imported file that is exclusively locked by another program or has permission restrictions, **When** `#btnRefresh` is clicked, **Then** the application catches `PermissionError` / `IOError` and displays an error toast ("Cannot refresh: File '<filename>' is locked or inaccessible.").
4. **Given** a corrupted or invalid workbook file, **When** `#btnRefresh` is clicked, **Then** the application catches `openpyxl.utils.exceptions.InvalidFileException` / general exceptions and displays an error toast without resetting valid workspace state.

---

### User Story 3 - Dirty State & Unsaved Changes Protection (Priority: P3)

As a user who has made unsaved hierarchy edits in the workspace, I want the refresh button to protect against accidental data loss by prompting whether to save changes to the template or discard them before reloading from disk.

**Why this priority**: Prevents accidental loss of user work during hierarchy design.

**Independent Test**: Make manual edits in the workspace tree (marking session dirty); click `#btnRefresh`. Verify `#unsavedModal` appears offering "Update Template & Refresh" / "Discard & Refresh".

**Acceptance Scenarios**:
1. **Given** a session with unsaved hierarchy changes (`isDirty == true`), **When** `#btnRefresh` is clicked, **Then** `#unsavedModal` is displayed asking whether to save or discard before refreshing.
2. **Given** the unsaved modal is displayed, **When** the user clicks "Discard & Refresh", **Then** in-memory changes are discarded and the file is refreshed from disk.
3. **Given** the unsaved modal is displayed, **When** the user clicks "Update Template & Refresh", **Then** changes are synced to the template before reloading the file.

---

## Edge Cases

- **No file session loaded**: `#btnRefresh` gracefully informs the user without error.
- **Active sheet deleted in external Excel**: Defaults to sheet index 0.
- **Empty workbook (0 sheets or all sheets blank)**: Catches empty workbook state and warns user without crashing.
- **Multi-sheet consistency**: Refreshes all sheets' headers and metadata simultaneously.
- **Template path binding**: Preserves or updates bound `current_template_path` properly.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Backend MUST expose a dedicated RPC endpoint `@eel.expose def refresh_excel_session() -> Dict[str, Any]` in `src/app/eel_bridge.py`.
- **FR-002**: `refresh_excel_session` MUST verify that `current_file_path` is set and exists on disk before attempting to read.
- **FR-003**: `refresh_excel_session` MUST catch and handle all filesystem and openpyxl exceptions (`FileNotFoundError`, `PermissionError`, `IOError`, `openpyxl.utils.exceptions.InvalidFileException`, `Exception`), returning `{ success: False, error: "..." }`.
- **FR-004**: `refresh_excel_session` MUST re-read all sheets using `ExcelHierarchyAdapter.read_row1_headers_and_types()` in strict Row-1 streaming mode (`max_row=1`).
- **FR-005**: If the currently active sheet (`current_active_sheet`) exists in the refreshed workbook, it MUST remain active; otherwise, it MUST default to the first sheet (`sheets[0]`).
- **FR-006**: Frontend `app.js` `refreshWorkspace()` MUST check `isDirty` state; if dirty, prompt via `#unsavedModal` with `pendingAction = { type: 'refresh_file' }`.
- **FR-007**: Frontend `app.js` MUST call `eel.refresh_excel_session()`, update all UI components (active sheet selector, catalog sheet selector, tree canvas, sidebar catalog, path list, counters), and display appropriate toast notifications (success / warning / error).
- **FR-008**: If no file is loaded, clicking `#btnRefresh` MUST display a warning toast: "No active Excel session loaded to refresh."

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of external file modifications (renamed headers, added columns, changed formats, added sheets) in the active file are reflected upon clicking `#btnRefresh`.
- **SC-002**: 100% of file exceptions (missing file, permission error, corrupted file, empty file) are caught gracefully with zero unhandled backend exceptions or UI freezes.
- **SC-003**: Refresh execution completes in < 500ms using strictly Row-1 streaming.
- **SC-004**: 100% passing test suite across all new and existing unit and integration tests.

---

## Assumptions

- The active Excel file path is tracked in `current_file_path` during the application session.
- Re-reading from disk reflects the latest saved state of the file in the operating system.
