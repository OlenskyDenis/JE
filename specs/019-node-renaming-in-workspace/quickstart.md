# Quickstart & Verification Guide: In-Place / Modal Node Renaming in Workspace

**Feature**: 019-node-renaming-in-workspace  
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

### Step 2: Create a Hierarchy Tree
1. Click **Create Root Node** (or import a file).
2. Name the root node `"Company"`.
3. Add a child node `"Finance"`.
4. Add a leaf node `"Q1_Budget"` under `"Finance"`.

### Step 3: Rename Node via Pencil Button
1. Hover over the `"Finance"` card.
2. Click the pencil edit button ✏️ (`.btn-node-edit`).
3. Verify the modal opens titled **Edit Node Name** with `"Finance"` pre-filled and highlighted.
4. Type `"Accounting"` and press `Enter`.
5. Confirm:
   - The node text changes to `"Accounting"`.
   - The child leaf path in the Export Preview tab updates to `"Company\Accounting\Q1_Budget"`.
   - `isDirty` is set to `true`.

### Step 4: Rename Node via Double-Click
1. Double-click on the label `"Q1_Budget"`.
2. Verify the modal opens pre-filled with `"Q1_Budget"`.
3. Type `"Annual_Report_2026"` and click **Save Changes**.
4. Confirm the label updates immediately.

### Step 5: Test Validation & Cancellation
1. Double-click on `"Company"`.
2. Clear the text so it is empty and press `Enter`.
3. Verify an error toast appears: `"Node name cannot be empty."` and the modal stays or cancels safely.
4. Press `Escape` and verify `"Company"` remains unchanged.
