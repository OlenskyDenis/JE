# Quickstart & Verification Guide: Hierarchical Excel Header Import

**Feature**: 006-excel-hierarchical-import  
**Date**: 2026-08-14  

## 1. Automated Verification (TDD)

Run pytest to execute the complete test suite including new path parser tests:

```powershell
python -m pytest
```

## 2. End-to-End Manual Verification Workflow

1. **Launch the Application**:
   ```powershell
   python -m src.app.main
   ```

2. **Import Excel File**:
   - Click **Import Excel** in the header actions bar.
   - Choose an `.xlsx` workbook that contains backslash headers in Row 1 (e.g. `hierarchy_export.xlsx` or a custom test file with `Root\Folder\Leaf`).

3. **Verify Canvas Tree Auto-Generation**:
   - Confirm that the tree canvas on the left is immediately populated with `Root -> Folder -> Leaf`.
   - Confirm node count badge updates appropriately.
   - Confirm the live Leaf Path Inspector lists the reconstructed path.

4. **Verify Sheet Switching**:
   - If the workbook has multiple sheets, switch to another sheet using the sheet selector dropdown.
   - Confirm that the workspace canvas tree immediately updates to display the new sheet's parsed hierarchy.

5. **Verify Export**:
   - Click **Export Excel**, save to a new file, and verify that Row 1 contains the expected leaf paths.
