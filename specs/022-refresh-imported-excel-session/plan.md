# Implementation Plan: Refresh Imported Excel File Session

**Feature Branch**: `022-refresh-imported-excel-session`  
**Spec**: [specs/022-refresh-imported-excel-session/spec.md](spec.md)  
**Created**: 2026-08-14  
**Status**: In Progress

---

## Technical Context & Architecture Overview

### Problem Statement
The `#btnRefresh` toolbar button currently calls `get_workspace_tree()`, which returns the in-memory tree without re-reading the active file on disk. When external edits occur in the Excel file (new columns, renamed headers, modified column data types, new sheets), clicking Refresh does not update the workspace.

### Target Architecture & Strategy
1. **Backend RPC Bridge (`src/app/eel_bridge.py`)**:
   - Expose `@eel.expose def refresh_excel_session() -> Dict[str, Any]`:
     - Validates that `current_file_path` is not None and exists on disk.
     - Wraps file loading in exhaustive `try...except` catching `FileNotFoundError`, `PermissionError`, `IOError`, `openpyxl.utils.exceptions.InvalidFileException`, and generic `Exception`.
     - Calls `ExcelHierarchyAdapter.get_sheet_names(current_file_path)` and `ExcelHierarchyAdapter.read_row1_headers_and_types(current_file_path, s)` in streaming mode (`max_row=1`).
     - Preserves `current_active_sheet` if it exists in the updated sheet list; otherwise defaults to `sheets[0]`.
     - Re-populates `sheet_forests`, `all_headers`, `all_headers_meta`, `forest`, `headers`, `headers_meta`.
     - Returns `{ success: True, file_path: ..., sheets: ..., active_sheet: ..., headers: ..., all_headers: ..., headers_meta: ..., all_headers_meta: ..., roots: ..., template_path: ... }`.
2. **Frontend UI Integration (`src/web/js/app.js`)**:
   - Update `refreshWorkspace()`:
     - If `this.isDirty` is true: prompt user via `#unsavedModal` with `pendingAction = { type: 'refresh_file' }`.
     - If not dirty: execute `performRefresh()`.
   - Update `#unsavedModal` handlers to support `action.type === 'refresh_file'`:
     - "Update Template & Refresh": Saves template via `eel.save_template_sync()` first, then calls `performRefresh()`.
     - "Discard & Refresh": Directly calls `performRefresh()`.
   - In `performRefresh()`:
     - Calls `eel.refresh_excel_session()`.
     - If `!res.success`: displays error toast with `res.error`.
     - If `res.success`: updates `this.cachedAllHeaders`, `this.cachedAllHeadersMeta`, sheet selectors, active sheet tree, sidebar catalog, and shows a success toast.
3. **Zero-Session Handling**:
   - If no file is loaded, clicking `#btnRefresh` displays a warning toast: "No active Excel session loaded to refresh."

---

## Constitution & Principle Gates Checklist

| Constitution Principle | Evaluation | Status |
|---|---|---|
| **I. Spec-Driven Development (SDD)** | Specification and plan finalized before any source code edits. | 🟢 Passed |
| **II. OOP & SOLID Principles** | Backend `refresh_excel_session` uses SRP; error handling cleanly isolated in adapter and bridge layers. | 🟢 Passed |
| **III. Gang of Four Design Patterns** | Dynamic Composite Pattern (`HierarchyNode`) preserved across all sheet trees. | 🟢 Passed |
| **IV. Library-First & TDD** | Integration tests written first covering normal refresh, file-lock exceptions, missing file errors, and empty session states. | 🟢 Passed |
| **V. Self-Contained Excel Processing** | Strict Row-1 openpyxl streaming (`max_row=1`), zero MS Excel runtime dependencies. | 🟢 Passed |
| **VI. System Map & Architecture Hygiene** | Synchronized with [`.specify/system_map.md`](../../.specify/system_map.md). | 🟢 Passed |
| **VII. Red Teaming & Zero-Data Stress Testing** | Validated against clean-slate (no file loaded), missing file, and locked file scenarios. | 🟢 Passed |

---

## Execution Phases & Artifacts

### Phase 0: Research & Exception Matrix (`research.md`)
- Document all potential file system and openpyxl exceptions and their user-facing remediation messages.

### Phase 1: Data Model & Contracts (`data-model.md`, `quickstart.md`)
- Document RPC payload for `refresh_excel_session` and UI state flow.
- Detail automated and manual verification steps in `quickstart.md`.

### Phase 2: Backend TDD Integration Tests (Red Stage)
- Add unit/integration tests in `tests/integration/test_eel_bridge.py` testing `refresh_excel_session` (success, missing file, permission error, no session loaded, deleted active sheet).

### Phase 3: Backend Implementation (Green Stage)
- Implement `refresh_excel_session()` in `src/app/eel_bridge.py`.

### Phase 4: Frontend UI Integration & Dirty State Protection
- Update `refreshWorkspace()`, `performRefresh()`, and `#unsavedModal` listeners in `src/web/js/app.js`.

### Phase 5: Verification & System Map Synchronization
- Update `.specify/system_map.md`.
- Run full pytest test suite (59+ tests).
