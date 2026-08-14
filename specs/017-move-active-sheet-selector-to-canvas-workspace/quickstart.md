# Quickstart & Verification Guide: Move Active Workspace Sheet Selector to Canvas Workspace

**Feature**: 017-move-active-sheet-selector-to-canvas-workspace  
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
1. Observe the left panel header contains:
   - Title: `Hierarchy Constructor Workspace`
   - Disabled inline dropdown: `Sheet: [(No Sheet)]`
   - Node counter: `0 Nodes`
   - Expand All / Collapse All buttons

2. Observe the right sidebar Tab 1 contains:
   - Single dropdown: `Browse Headers From: [(No Sheet Loaded)]`
   - Search input
   - Empty state

### Step 2: Import Multi-Sheet File
1. Click **Import Excel** and select a file with sheets `Sales` and `Inventory`.
2. Observe the left panel header dropdown updates to show `Sheet: [Sales ▾]`.
3. Observe the right sidebar dropdown shows `Browse Headers From: [Sales ▾]`.

### Step 3: Switch Active Sheet from Canvas Header
1. In the left panel header, change `Sheet:` dropdown to `Inventory`.
2. Confirm the workspace canvas immediately updates to show `Inventory`'s hierarchy.
3. Add a node `Warehouse_Zone_A` to `Inventory`.

### Step 4: Verify Unsaved Changes Protection on Canvas Switch
1. In the left panel header, select `Sales`.
2. Confirm the Unsaved Changes confirmation modal appears.
3. Click **Cancel** — confirm workspace remains on `Inventory`.
4. Select `Sales` again and click **Update Template & Switch** (or **Discard & Switch**) — confirm canvas switches cleanly.

### Step 5: Verify Cross-Sheet Dragging
1. With `Sales` active on canvas, set the sidebar dropdown **Browse Headers From:** to `All Sheets (Combined)`.
2. Drag a header from `Inventory` onto the `Sales` tree on the canvas.
3. Confirm the canvas accepts the node without changing the canvas active sheet.
