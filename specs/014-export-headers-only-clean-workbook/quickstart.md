# Quickstart & Verification Guide: Full-Workbook Header Template Export (`Шаблон_...xlsx`)

**Feature**: 014-export-headers-only-clean-workbook  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Workflow

### Step 1: Launch the Application
```powershell
python -m src.app.main
```

### Step 2: Prepare a Multi-Sheet Excel File with Data
1. Create a test workbook `Company_Data.xlsx` with:
   - Sheet `Sales`: Headers `["Region\\North", "Region\\South", "Revenue"]`, and 20 rows of data in Row 2-21.
   - Sheet `Employees`: Headers `["ID", "Name", "Department"]`, and 50 rows of data in Row 2-51.
2. Click **Import Excel** and select `Company_Data.xlsx`.

### Step 3: Reorganize and Export
1. On the `Sales` sheet, add or reorder nodes in the hierarchy tree.
2. Click **Export Excel**.
3. Verify the native save dialog proposes the default filename: `Шаблон_Company_Data.xlsx`.
4. Choose a destination and click Save.

### Step 4: Inspect the Exported File
1. Open the saved `Шаблон_Company_Data.xlsx` file in Excel or inspect with Python.
2. Confirm:
   - Both sheets `Sales` and `Employees` exist in exact sequence.
   - `Sales` sheet contains only Row 1 with the reorganized leaf paths, and exactly 0 rows of data (`max_row == 1`).
   - `Employees` sheet contains only Row 1 with `ID`, `Name`, `Department`, and exactly 0 rows of data (`max_row == 1`).
   - All rows below Row 1 are completely empty across the entire workbook.
