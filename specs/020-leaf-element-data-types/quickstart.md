# Quickstart & Verification Guide: Leaf Element Data Types

**Feature**: 020-leaf-element-data-types  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite:

```powershell
python -m pytest
```

Ensure 100% pass rate with zero test failures.

---

## 2. End-to-End Manual Verification Workflow

### Step 1: Launch Application
```powershell
python -m src.app.main
```

### Step 2: Test Clean-Slate Creation & Type Assignment
1. In the Hierarchy Constructor Workspace canvas, click **Create Root Node**.
2. Set name to `"Products"`.
3. Add a child node `"Price"`.
4. Click edit ✏️ (or double-click) on `"Price"`.
5. Select **Currency** in the *Element Data Type* dropdown and click **Save Changes**.
6. Verify:
   - Node `"Price"` displays a `[Currency]` badge.
   - In the **Export Preview** tab, `"Products\Price"` displays with `[Currency]`.
   - `isDirty` is set to `true`.

### Step 3: Test Dynamic Folder-to-Leaf Transformation upon Deletion
1. Add a child node `"Tax"` under `"Price"` (this upgrades `"Price"` to a folder).
2. Observe that `"Price"` no longer displays a data type badge (it is now a folder).
3. Delete `"Tax"`.
4. Observe that `"Price"` dynamically transforms back into a leaf element:
   - The `[Currency]` (or `[Text]`) badge immediately reappears.
   - Editing `"Price"` enables the data type selector.
   - `"Products\Price"` appears in **Export Preview**.

### Step 4: Test Excel Import Type Inference & Catalog Drag-and-Drop
1. Click **Import Excel** and select a multi-column Excel spreadsheet.
2. Observe that imported leaf nodes display their auto-detected data types (`[Date]`, `[Currency]`, `[Integer]`, `[Text]`, etc.).
3. Drag a header (e.g. `HireDate` with Date type) from the **Header Catalog** into the canvas.
4. Verify the newly created node automatically inherits the `[Date]` type without manual configuration.

### Step 5: Test Excel Export Persistence
1. Click **Export Excel** and save the template as `Шаблон_test_export.xlsx`.
2. Inspect the saved Excel file.
3. Verify:
   - Row 1 contains the leaf path headers.
   - Each column has the appropriate Excel number format (`$#,##0.00` for Currency, `yyyy-mm-dd` for Date, `0` for Integer, `@` for Text).
