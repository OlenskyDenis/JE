# Quickstart & End-to-End Validation Guide

**Feature**: `002-excel-sidebar-reorganizer`  
**Date**: 2026-08-13  
**Status**: Complete  

---

## Prerequisites

- **Python**: Python 3.10+ installed
- **Dependencies**: `openpyxl`, `eel`, `pytest` installed via `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

---

## Running Unit & Integration Verification

To run automated tests for header extraction, multi-sheet switching, and horizontal Row 1 export:

```bash
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

---

## Manual End-to-End UI Validation

1. **Launch Desktop App**:
   ```bash
   python -m src.app.main
   ```
2. **Import Multi-Sheet Excel File**:
   - Click **Import Excel** button.
   - Select a sample `.xlsx` file containing multiple sheets (e.g., `Sheet1`, `Sheet2`).
3. **Verify Sheet Selector & Sidebar**:
   - Confirm the sheet dropdown list displays all sheet names.
   - Check that the sidebar displays unique headers extracted exclusively from Row 1 of the active sheet, sorted alphabetically.
   - Type in the sidebar search input and verify that items filter instantaneously in real-time.
   - Select a different sheet in the dropdown and verify the sidebar updates immediately to display headers from the new sheet.
4. **Test Non-Destructive Drag-and-Drop**:
   - Drag a header item from the sidebar into the main tree constructor canvas.
   - Verify a new tree node is created.
   - Confirm the dragged header remains in the sidebar list and can be dragged again.
5. **Test Re-Export**:
   - Click **Export to Excel**.
   - Open the exported `.xlsx` file in Excel or inspect programmatically.
   - Verify Row 1 contains leaf node backslash path strings (`Root\Folder\Item`) written horizontally across columns A1, B1, C1...
   - Confirm unedited sheets and lower rows retain their original contents.
