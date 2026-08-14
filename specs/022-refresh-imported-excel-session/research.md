# Technical Research: Exception Handling & Session Refresh Architecture

**Feature Branch**: `022-refresh-imported-excel-session`  
**Spec**: [specs/022-refresh-imported-excel-session/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Exception Scenarios & Handling Matrix

| Exception Scenario | Python Exception Type | Backend Handling Strategy | Frontend Toast UI Response |
|---|---|---|---|
| **No File Loaded** | `None` check on `current_file_path` | Returns `{"success": False, "error": "No active Excel session loaded to refresh."}` | `Warning` toast: "No active Excel session loaded to refresh." |
| **File Deleted / Moved on Disk** | `FileNotFoundError` | Catches error; returns `{"success": False, "error": f"Cannot refresh: File '{path}' not found."}` | `Error` toast: "Cannot refresh: File '<filename>' not found." |
| **File Locked by Another Process (e.g. MS Excel exclusive write lock)** | `PermissionError`, `IOError` | Catches error; returns `{"success": False, "error": f"Cannot refresh: File '{path}' is locked by another process."}` | `Error` toast: "Cannot refresh: File '<filename>' is locked by another process." |
| **Corrupted / Invalid Excel File Format** | `openpyxl.utils.exceptions.InvalidFileException`, `zipfile.BadZipFile` | Catches error; returns `{"success": False, "error": "Invalid or corrupted Excel file."}` | `Error` toast: "Invalid or corrupted Excel file." |
| **Empty Workbook (0 Sheets / 0 Headers)** | Empty `sheetnames` list | Catches empty state; returns `{"success": False, "error": "Workbook contains no valid worksheets."}` | `Warning` toast: "Workbook contains no valid worksheets." |
| **Active Sheet Removed Externally** | Key not in `sheetnames` | Automatically falls back to `sheets[0]` and rebuilds active tree | `Info` toast: "Active sheet was deleted; switched to '<first_sheet>'." |

---

## 2. Dirty State & Accidental Data Loss Prevention

When the user modifies the hierarchy in the canvas, `isDirty = true`.
If the user clicks `#btnRefresh`:
1. `app.js` checks `if (this.isDirty)`.
2. Intercepts the click and displays `#unsavedModal` with:
   - Message: `"You have unsaved changes in your current session. Reloading the file will discard these changes. Save to template before refreshing or Discard & Refresh?"`
   - Buttons: `[Update Template & Refresh]` (`#btnUnsavedSave`) and `[Discard & Refresh]` (`#btnUnsavedDiscard`).
3. `pendingAction = { type: 'refresh_file' }` coordinates the chosen resolution.
