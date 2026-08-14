# Quickstart & Verification Guide: Multi-Sheet Session Persistence & Template Auto-Sync

**Feature**: 016-multi-sheet-session-persistence-and-template-sync  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Workflow

### Step 1: Launch Application
```powershell
python -m src.app.main
```
1. Observe the header toolbar displays `#templateStatusBadge`: `Template: (None)`.

### Step 2: Import Multi-Sheet Excel File
1. Click **Import Excel** and select a file with sheets `Sales` and `Inventory`.
2. On `Sales`, add a custom node `Sales_Branch_Alpha`.
3. In the Unsaved Changes modal (or click Export Excel), save to `Шаблон_Company_2026.xlsx`.
4. Confirm:
   - `#templateStatusBadge` updates to `Template: Шаблон_Company_2026.xlsx (Synced)`.

### Step 3: Switch Sheets & Modify Another Sheet
1. Switch **Active Workspace Sheet** to `Inventory`.
2. Add a custom node `Warehouse_Zone_1`.
3. Observe `isDirty` is set for `Inventory`.

### Step 4: Verify 1-Click Template Sync
1. In **Active Workspace Sheet**, select `Sales`.
2. The modal prompts:
   - Message: *"You have unsaved changes on sheet 'Inventory'. Update template 'Шаблон_Company_2026.xlsx' before switching to 'Sales'?"*
   - Button: `[Update Template & Switch]`.
3. Click **Update Template & Switch**:
   - Confirm the update executes instantly without opening the OS file dialog!
   - Confirm workspace switches back to `Sales`.

### Step 5: Verify Session Persistence & Restored Trees
1. Verify that `Sales` tree displays `Sales_Branch_Alpha` fully intact!
2. Switch back to `Inventory`:
   - Verify `Inventory` tree displays `Warehouse_Zone_1` fully intact!

### Step 6: Verify Exported File Quality
1. Open `Шаблон_Company_2026.xlsx`:
   - Verify `Sales` contains Row 1 headers including `Sales_Branch_Alpha`.
   - Verify `Inventory` contains Row 1 headers including `Warehouse_Zone_1`.
   - Verify `max_row == 1` and zero data rows exist across all sheets.
