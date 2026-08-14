# Quickstart & Verification Guide: Intuitive Sheet Management, Unsaved Changes Protection & Cross-Sheet Header Catalog

**Feature**: 015-sheet-manager-save-prompt-and-cross-sheet-catalog  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Workflow

### Step 1: Launch Application & Verify Initial Badges
```powershell
python -m src.app.main
```
1. Observe the workspace header displays:
   - `Hierarchy Constructor Workspace`
   - `#activeSheetBadge`: `Active Sheet: (None)` (or `Scratch Session`).
2. Observe Tab 2 is clearly labeled `Export Preview`.

### Step 2: Import Multi-Sheet File
1. Click **Import Excel** and load a file with sheets `Sales` and `Inventory`.
2. Confirm:
   - `#activeSheetBadge` updates to `Active Sheet: Sales`.
   - `#activeSheetSelector` is set to `Sales`.
   - `#catalogSheetSelector` is set to `Sales` (with options for `All Sheets (Combined)`, `Sales`, `Inventory`).

### Step 3: Verify Cross-Sheet Header Catalog Browsing
1. While `Sales` is active on the canvas, select `Inventory` in **Browse Headers From** (`#catalogSheetSelector`).
2. Confirm:
   - The sidebar header list immediately displays headers from `Inventory`.
   - The workspace canvas remains on `Sales` without reloading or losing nodes.
3. Drag a header from `Inventory` into the `Sales` tree canvas.
4. Confirm the node is added to `Sales` tree and `isDirty` is set.

### Step 4: Verify Unsaved Changes Protection
1. In **Active Workspace Sheet** (`#activeSheetSelector`), select `Inventory`.
2. Confirm the **Unsaved Changes** modal appears:
   - Message: *"You have unsaved changes in the Hierarchy Constructor Workspace for sheet 'Sales'..."*
3. Click **Cancel**:
   - Confirm modal closes.
   - Confirm workspace remains on `Sales` with all added nodes intact.
   - Confirm `#activeSheetSelector` resets back to `Sales`.
4. Select `Inventory` again and click **Discard & Switch**:
   - Confirm workspace switches to `Inventory` and `#activeSheetBadge` updates to `Active Sheet: Inventory`.
