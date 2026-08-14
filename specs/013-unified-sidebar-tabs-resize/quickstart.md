# Quickstart & Verification Guide: Unified Tabbed Sidebar & Draggable Left-Edge Resizing

**Feature**: 013-unified-sidebar-tabs-resize  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite to confirm zero backend or integration regressions:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual UI Verification Workflow

### Step 1: Launch the Application
```powershell
python -m src.app.main
```

### Step 2: Verify Initial 2-Column Layout & Default Tab
1. Observe that the workspace displays exactly two top-level columns:
   - Left: **Hierarchy Constructor Workspace** (expanded horizontal room).
   - Right: **Unified Sidebar Panel**.
2. Verify the **Excel Header Catalog** tab is active by default.
3. Verify both tab buttons display live badge counts:
   - "Header Catalog": `0 Headers`
   - "Leaf Paths": `0 Paths`

### Step 3: Verify Tab Switching & Live Counter Updates
1. Click "Import Excel" and load a sample spreadsheet (or create root nodes manually).
2. Confirm the "Header Catalog" badge displays the count of unique headers (e.g. `12 Headers`).
3. Confirm the "Leaf Paths" badge displays the count of generated leaf paths (e.g. `5 Paths`).
4. Click on the **Leaf Paths** tab:
   - View instantly switches to display generated path cards (`#pathList`).
   - Active tab indicator shifts to the Leaf Paths tab.
5. Click back on the **Header Catalog** tab:
   - View instantly restores Sheet Manager, Search box, and header items.
   - Any previously typed search query remains present and filtered.

### Step 4: Verify Draggable Left-Edge Resizing
1. Hover over the left border of the unified sidebar.
2. Confirm the cursor changes to `col-resize` and the accent highlight line appears.
3. Click and drag the left edge to the left (expanding the sidebar to ~500px):
   - Confirm sidebar widens smoothly and the tree canvas contracts in real time.
   - Confirm text selection is suppressed during dragging.
4. Release the mouse.
5. Drag to the far right (towards minimum width):
   - Confirm resizing clamps smoothly at `260px` minimum.
6. Drag to the far left (towards maximum width):
   - Confirm resizing clamps before tree canvas becomes smaller than `320px`.
7. Double-click the left resize handle:
   - Confirm the sidebar instantly resets to the standard `340px` default width.

### Step 5: Verify Persistence Across Reloads
1. Resize the sidebar to a custom width (e.g., ~450px).
2. Refresh the application window (`Ctrl+R` or restart the app).
3. Confirm the sidebar restores at the custom ~450px width from `localStorage`.

### Step 6: Verify Drag & Drop and Excel Export Across Tabs
1. While on the **Header Catalog** tab, drag a header item into the tree canvas:
   - Confirm 3-zone drop targets and node addition work seamlessly.
2. While on the **Header Catalog** tab, click **Export Excel**:
   - Confirm leaf paths are accurately exported to Row 1 without needing to switch to the Leaf Paths tab first.
