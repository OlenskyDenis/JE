# Feature Specification: Unified Tabbed Sidebar & Draggable Left-Edge Resizing

**Feature Branch**: `013-unified-sidebar-tabs-resize`  
**Created**: 2026-08-14  
**Status**: Draft (Clarified & Aligned with System Map)  

**Input**: User directive: "Combine Leaf Node Absolute Paths and Excel Header Catalog into a single element, add the ability to switch between them, and add the ability to resize this element by dragging its left edge"

---

## Constitution Compliance & System Map Audit
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (Modular UI & State Cleanliness)**: Clear separation of concerns between tab state management, resizing controller logic, path rendering, and catalog rendering without polluting global application state.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) loaded and consulted. Consolidates the existing 3-column layout (`tree-panel`, `path-panel`, `sidebar-panel`) into a 2-column layout (`tree-panel`, `unified-sidebar-panel`) while preserving all existing DOM capabilities, IDs, and event handlers.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validated for zero-data states (no file loaded, empty tree), high-density data (hundreds of headers/paths), rapid tab toggling, boundary-crossing drag resizes, and viewport adjustments.

### Connected Elements & Impact Analysis (System Map Trace)

| Layer / Component | File / Target | System Map Role | Specific Feature 013 Impact & Preservation Strategy |
|---|---|---|---|
| **Layout & Markup** | [`src/web/index.html`](file:///E:/JE/src/web/index.html) | Workspace Grid & Panels | Replaces 3-panel markup (`path-panel` and `sidebar-panel`) with a single `<section class="panel unified-sidebar-panel" id="unifiedSidebar">`. Houses Tab Bar (`#tabBtnCatalog`, `#tabBtnPaths`), view containers (`#tabContentCatalog`, `#tabContentPaths`), and resizer handle (`#sidebarResizer`). All critical IDs (`#sheetSelector`, `#sidebarSearch`, `#sidebarHeaderList`, `#sidebarEmptyState`, `#headerCountBadge`, `#pathList`, `#pathCountBadge`) are preserved. |
| **Styling System** | [`src/web/css/style.css`](file:///E:/JE/src/web/css/style.css) | Dark Theme Design Tokens | Replaces `.three-column-layout` with a 2-column layout (`tree-panel` flex-grow, `unified-sidebar-panel` resizable width). Adds styles for tabs, active state indicators, `.resizer-handle-left`, and `body.is-resizing` (`cursor: col-resize; user-select: none`). |
| **Drag & Drop** | [`src/web/js/drag_drop.js`](file:///E:/JE/src/web/js/drag_drop.js) | Three-Zone Hit Testing | Non-destructive drag from `#sidebarHeaderList` into `#treeView` remains 100% operational when the Catalog tab is active. Resizer handle uses pointer capture to prevent conflicting with tree node or header drags. |
| **Tree & Path Renderer**| [`src/web/js/tree_renderer.js`](file:///E:/JE/src/web/js/tree_renderer.js)| Node & Path DOM Generator | `TreeRenderer.renderPaths(roots, this.pathListEl)` continues rendering `.path-card` elements into `#pathList` and updating `#pathCountBadge` seamlessly, whether the Paths tab is currently active or inactive. |
| **App Controller** | [`src/web/js/app.js`](file:///E:/JE/src/web/js/app.js) | Frontend State & Eel RPC Dispatcher | Integrates `TabController` and `SidebarResizeController`. Keeps `pathListEl` in the DOM so `handleExportReorganizedRow1` (`this.pathListEl.querySelectorAll('.path-card')`) exports leaf paths accurately without DOM detachment issues. Persists sidebar width to `localStorage`. |
| **Backend RPC & Core**| [`src/app/eel_bridge.py`](file:///E:/JE/src/app/eel_bridge.py) | Python Domain Bridge | Zero backend modifications required; all RPC endpoints (`get_workspace_tree`, `import_excel_file`, `switch_active_sheet`, `export_reorganized_row1`) continue operating seamlessly. |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Unified Tabbed Side Panel with View Switching (Priority: P1) 🎯 MVP

As a database architect working with large hierarchy trees, I want the "Excel Header Catalog" and "Leaf Node Absolute Paths" views merged into a single tabbed side panel on the right, so that my primary tree canvas has more horizontal space while letting me easily switch between browsing source headers and inspecting generated leaf paths.

**Why this priority**: Core layout and structural requirement that consolidates two separate panels into a clean, modern tabbed element.

**Independent Test**: Load the application and verify that a single right-hand panel exists with two distinct tabs: "Excel Header Catalog" and "Leaf Paths". Clicking each tab switches the visible panel content and updates the active tab styling without breaking any header catalog search or leaf path preview functionality.

**Acceptance Scenarios**:

1. **Given** the workspace is rendered, **When** examining the layout, **Then** there are exactly two primary top-level layout columns: the Hierarchy Constructor Workspace on the left and the Unified Tabbed Sidebar on the right.
2. **Given** the application opens on initial launch, **When** loading the unified sidebar, **Then** the "Excel Header Catalog" tab is active by default, displaying the Excel Sheet selector, Header Search bar, and draggable Header list.
3. **Given** the unified sidebar, **When** clicking on the "Leaf Node Paths" tab, **Then** the view switches to display the list of full backslash-delimited leaf node paths (`#pathList`).
4. **Given** an imported Excel file or dynamic tree edits, **When** the underlying data updates, **Then** the badge counters on both tabs (`#headerCountBadge` and `#pathCountBadge`) accurately reflect current counts simultaneously regardless of which tab is currently active.
5. **Given** the Excel Header Catalog tab is active, **When** the user clicks "Export Excel", **Then** the system successfully reads the generated leaf paths from `#pathList` in the DOM and exports Row 1 columns without requiring the user to manually switch tabs.

---

### User Story 2 - Draggable Left-Edge Panel Resizing with Persistence (Priority: P2)

As a power user working on varied display resolutions or deeply nested path structures, I want to resize the right-hand panel by dragging its left border, so that I can expand it to inspect long path strings or shrink it to give more room to the hierarchy tree, and have my preferred width remembered.

**Why this priority**: Directly requested functionality essential for usability with variable header and path lengths.

**Independent Test**: Hover over the left border of the unified side panel, verify the `col-resize` cursor appears, click and drag the border to the left, and observe the panel expanding smoothly while the tree canvas contracts. Refresh the page/session and verify the width is preserved.

**Acceptance Scenarios**:

1. **Given** the mouse hovers over the resizer handle on the left edge of the unified panel (`#sidebarResizer`), **When** positioned within the hit target zone (6-8px width), **Then** the cursor changes to `col-resize` with visual hover feedback (accent highlight).
2. **Given** the user presses down (`mousedown` / `pointerdown`) on the left resize handle and drags horizontally, **When** moving the pointer, **Then** the unified sidebar width updates in real-time to match the cursor position relative to the right edge of the viewport/container.
3. **Given** dragging is in progress, **When** the cursor moves across text or input fields, **Then** text selection and unintended drag-and-drop operations are suppressed (`user-select: none; pointer-events: none` on inner frames/cards).
4. **Given** dragging reaches minimum or maximum boundary limits (min 260px, max 70% of viewport width / preserving minimum 320px for tree canvas), **When** moving beyond those limits, **Then** panel resizing clamps safely at the boundary without overflowing.
5. **Given** dragging completes (`mouseup` / `pointerup`), **When** releasing the pointer, **Then** resizing mode terminates cleanly, restoring normal event handling, and the new width is stored in `localStorage` (`app_sidebar_width`).
6. **Given** the user double-clicks on the resize handle, **When** triggered, **Then** the sidebar width resets to the default standard width (340px).

---

### User Story 3 - Full Drag-and-Drop and State Preservation Across Tabs (Priority: P3)

As a user organizing catalog items into the hierarchy, I want drag-and-drop from the Header Catalog tab into the canvas tree to remain completely frictionless, and my active search queries and sheet selections to remain intact when switching tabs.

**Why this priority**: Guarantees zero regressions to existing core workflows (Feature 002, 005, 008, 011).

**Independent Test**: In the Excel Header Catalog tab, filter headers by typing in the search box, switch to the Leaf Paths tab, switch back to the Header Catalog tab, and verify that the filter text, filtered results, and selected sheet remain intact. Drag an item from the catalog tab into the tree canvas and confirm insertion succeeds.

**Acceptance Scenarios**:

1. **Given** a filtered header list in the Header Catalog tab, **When** switching to the Leaf Paths tab and back, **Then** the search input value and filtered list state are preserved without re-filtering or resetting.
2. **Given** the Header Catalog tab is active, **When** initiating a drag from a header item into the hierarchy tree canvas, **Then** three-zone drop targets (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) and visual feedback function identically to previous versions.
3. **Given** changes made in the tree canvas while in the Header Catalog tab, **When** switching to the Leaf Paths tab, **Then** the leaf paths list immediately reflects all recent changes without needing manual refresh.

---

## Edge Cases

- **Narrow Viewport Handling**: On screens narrower than 1024px, the max allowed sidebar width dynamically clamps to guarantee the main tree canvas retains at least 320px of usable workspace.
- **Fast Pointer Movement & Window Leave**: If the user rapidly drags outside the browser window and releases, global pointer/mouse capture (`pointerdown` with `setPointerCapture` or `window`-level listeners) ensures resizing cleanly concludes without getting stuck in a dragging loop.
- **Empty State Display in Inactive & Active Tabs**: Both tabs must render their respective empty states (`#sidebarEmptyState`, `#treeEmptyState`, or empty path state) appropriately when no workbook is loaded or tree is empty.
- **Double Click Reset**: Double-clicking the `#sidebarResizer` resets the sidebar width to the default standard 340px and updates `localStorage`.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The three-column workspace layout (`.workspace-main.three-column-layout`) MUST be replaced with a 2-column layout consisting of the tree workspace panel (`.tree-panel`) on the left and the unified sidebar (`.unified-sidebar-panel`) on the right.
- **FR-002**: The unified sidebar MUST include a tab header bar containing two selectable tabs:
  - Tab A: **Excel Header Catalog** (`#tabBtnCatalog` with `#headerCountBadge`).
  - Tab B: **Leaf Node Absolute Paths** (`#tabBtnPaths` with `#pathCountBadge`).
- **FR-003**: The tab header MUST display live badge counters for both tabs simultaneously regardless of which tab is currently selected.
- **FR-004**: Clicking a tab MUST switch visible views (`#tabContentCatalog` vs `#tabContentPaths`) using CSS visibility/display classes while keeping both view DOM trees intact in memory.
- **FR-005**: On initial startup, the default active tab MUST be the **Excel Header Catalog** tab.
- **FR-006**: A dedicated draggable resize splitter handle (`#sidebarResizer`) MUST be positioned along the entire left border of the unified sidebar.
- **FR-007**: Dragging `#sidebarResizer` MUST dynamically adjust the width of the unified sidebar in real-time, bound by strict minimum (260px) and maximum (clamp to 70% viewport or max tree width preservation) constraints.
- **FR-008**: When resizing is active, `document.body` MUST receive the class `is-resizing` to set `cursor: col-resize`, prevent text selection (`user-select: none`), and ensure smooth pointer tracking.
- **FR-009**: The resized width MUST be persisted to `localStorage` under `app_sidebar_width` and restored on subsequent application launches (fallback: 340px).
- **FR-010**: Double-clicking `#sidebarResizer` MUST reset the sidebar width to 340px.
- **FR-011**: Drag-and-drop operations from the Header Catalog into the Hierarchy Constructor Workspace MUST remain 100% operational with no hit-testing regressions.
- **FR-012**: `handleExportReorganizedRow1` MUST continue reading `.path-card` elements from `#pathList` regardless of which tab is currently active.
- **FR-013**: All UI styling MUST strictly follow the established dark theme design tokens (`--bg-main`, `--bg-panel`, `--bg-panel-header`, `--bg-card`, `--border-color`, `--color-primary`).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Main workspace layout is reduced from 3 static columns to 1 main tree canvas + 1 unified tabbed right panel, increasing initial default horizontal tree canvas space by at least 25%.
- **SC-002**: Tab switching between Header Catalog and Leaf Paths occurs instantaneously (< 16ms, 60fps) with 0 DOM rebuild delays.
- **SC-003**: Left-edge dragging resizes the sidebar smoothly without visual stuttering, layout breakage, or event dropouts across 100% of tested pointer drag trajectories.
- **SC-004**: Sidebar width preference is accurately persisted across page reloads in `localStorage`.
- **SC-005**: 100% of existing tests pass with 0 regressions (`python -m pytest`).

---

## Assumptions

- No Python backend RPC alterations are required for layout restructuring; all existing backend endpoints (`get_workspace_tree`, `import_excel_file`, `switch_active_sheet`, `export_reorganized_row1`, `add_node`, `move_node`, `delete_node`, `open_file_dialog`, `save_file_dialog`) continue to operate without change.
