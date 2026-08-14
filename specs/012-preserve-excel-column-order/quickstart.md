# Quickstart & Verification Guide: Preservation of Original Excel Column Sequence

**Feature**: 012-preserve-excel-column-order  
**Date**: 2026-08-14  

## 1. Automated Test Verification

Run all test suites to confirm that insertion order is verified and all tests pass:

```powershell
python -m pytest
```

## 2. End-to-End Manual Verification Workflow

1. **Start the Application**:
   ```powershell
   python -m src.app.main
   ```

2. **Prepare or Load an Excel File with Non-Alphabetical Headers**:
   - For example, Row 1 containing: `["Zebra\\Stripes", "Beta\\Sub", "Alpha\\Item"]`.
   - Click "Import Excel" and load the file.

3. **Verify Canvas Tree Node Sequence**:
   - Inspect the Hierarchy Constructor Workspace canvas.
   - Confirm root nodes are ordered: `Zebra` (first), `Beta` (second), `Alpha` (third).
   - Confirm nodes are NOT sorted alphabetically (`Alpha` -> `Beta` -> `Zebra`).

4. **Verify Sidebar and Leaf Paths Sequence**:
   - Inspect the right-hand sidebar ("Excel Header Catalog"). Confirm items match the original Excel column sequence.
   - Inspect the middle panel ("Leaf Node Absolute Paths"). Confirm path cards match the tree left-to-right order.
