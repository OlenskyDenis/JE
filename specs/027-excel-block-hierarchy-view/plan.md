# Implementation Plan: Excel Block Hierarchy View (Multi-Level Header Matrix Mode)

**Feature Branch**: `027-excel-block-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  
**Spec**: [specs/027-excel-block-hierarchy-view/spec.md](spec.md)  
**Research**: [specs/027-excel-block-hierarchy-view/research.md](research.md)  
**Data Model**: [specs/027-excel-block-hierarchy-view/data-model.md](data-model.md)  
**Quickstart**: [specs/027-excel-block-hierarchy-view/quickstart.md](quickstart.md)  

---

## 1. Executive Summary & Architecture

This feature introduces an alternative, human-readable visual display mode (**Excel Block Hierarchy View**) into the **Hierarchy Constructor Workspace**. The view renders multi-root tree structures as an interactive multi-tier spreadsheet block matrix mimicking Excel merged header cells (parents stacked on top with horizontal `colspan` equal to total leaf descendants, and nested children stacked beneath with terminal leaf `rowspan` vertical expansion).

---

## 2. Technical Scope & Implementation Phases

### Phase 1: Baseline Verification
- Run existing test suite (`python -m pytest`) to verify 75+ tests pass with zero regressions.

### Phase 2: Core Matrix Calculation & Rendering Engine (`src/web/js/excel_block_renderer.js`)
- Implement `ExcelBlockRenderer` object:
  - `getMaxDepth(roots)`: Computes maximum hierarchy depth.
  - `getLeafCount(node)`: Computes total leaf column width of a node or subtree.
  - `getExcelColumnLabel(colIndex)`: Converts 0-based column index to Excel column coordinate string (`A`, `B`, `...`, `Z`, `AA`, `AB`...).
  - `buildMatrixLayout(roots)`: Builds the 2D multi-tier matrix grid (`tierRows`, `colSpan`, `rowSpan`, `isLeaf`, `tooltip`).
  - `renderMatrix(roots, containerEl)`: Generates semantic HTML `<table>` markup with `<thead>` coordinate strip and multi-tier `<tbody>` block cells.
  - Generates rich hover tooltips with node name, absolute path, data type, and span statistics.

### Phase 3: Localization & Internationalization (`src/web/js/i18n.js`)
- Register Ukrainian (`uk`) and English (`en`) dictionary entries for:
  - `view_mode_tree`, `view_mode_matrix`
  - `tooltip_view_mode_tree`, `tooltip_view_mode_matrix`
  - `matrix_col_prefix`, `matrix_depth_label`, `matrix_colspan_label`
  - `matrix_empty_title`, `matrix_empty_hint`

### Phase 4: HTML Markup & Dark Theme CSS Styling
- Update [`src/web/index.html`](file:///E:/JE/src/web/index.html):
  - In `.workspace-sheet-picker`, add `#viewModeSwitcher` segmented control (`#btnViewTree` and `#btnViewMatrix`).
  - In `.workspace-canvas-body`, wrap view containers and add `<div id="excelBlockView" class="excel-block-view hidden"></div>`.
  - Include `<script src="js/excel_block_renderer.js"></script>`.
- Update [`src/web/css/style.css`](file:///E:/JE/src/web/css/style.css):
  - Add segmented view switcher styles (`.view-mode-switcher`, `.view-mode-btn`).
  - Add table matrix styles: `.excel-matrix-table`, `.matrix-coord-header`, `.matrix-cell`, `.matrix-cell-folder`, `.matrix-cell-leaf`.
  - Add hover elevation, cell borders, tier color fills, and responsive horizontal scroll container styles.

### Phase 5: App Controller Wiring & State Synchronization (`src/web/js/app.js`)
- In `App.bindDOM()`: Bind `#btnViewTree`, `#btnViewMatrix`, `#excelBlockView`.
- In `App.bindEvents()`: Wire click handlers for view switching.
- Implement `App.switchViewMode(mode)`:
  - Toggles active class on switcher buttons.
  - Toggles visibility of `#treeView` vs `#excelBlockView`.
  - Persists preference to `localStorage.setItem('je_workspace_view_mode', mode)`.
  - Calls `ExcelBlockRenderer.renderMatrix(this.currentRoots, this.excelBlockViewEl)`.
- In `App.init()`: Load saved view mode from `localStorage`.
- In `App.updateUI(roots)`: Call both `TreeRenderer.renderTree` and `ExcelBlockRenderer.renderMatrix`.

### Phase 6: System Map, Tasks & End-to-End Verification
- Update `.specify/system_map.md` with new `ExcelBlockRenderer` module and view switching capabilities.
- Run complete test suite (`python -m pytest`) to confirm 100% pass rate.

### Phase 7: Sidebar Collapse & Expand (Quick Fix Enhancement)
- Add collapse toggle button `#btnToggleSidebarCollapse` in `.sidebar-tab-header` and `.sidebar-collapsed-strip` with `#btnExpandSidebarStrip` in `#unifiedSidebar`.
- Add dark theme CSS for `.sidebar-collapsed` (width: 28px, custom cursor, smooth transition, collapsed strip layout).
- Update `SidebarResizeController` in `src/web/js/app.js` to support `toggleCollapse()`, width preservation, and `localStorage` persistence (`je_sidebar_collapsed`).
- Add Ukrainian and English dictionary keys for `sidebar_btn_collapse` and `sidebar_btn_expand` in `src/web/js/i18n.js`.
- Verify contract and integrity tests with `python -m pytest`.

### Phase 8: Unified Sidebar Tab Dropdown & Responsive Header Layout (Quick Fix Enhancement)
- Replace horizontal tab buttons in `.sidebar-tab-header` with a compact dropdown selector `#sidebarTabSelector` containing `catalog` and `paths` options and dynamic active count badge `#sidebarActiveBadge`.
- Ensure `#btnToggleSidebarCollapse` has `flex-shrink: 0` and is always visible and clickable at minimum manual sidebar widths.
- Update `bindTabs()` and `updateTabBadge()` in `src/web/js/app.js` to handle dropdown change events and active tab switching.
- Verify contract tests via `python -m pytest`.

---

## 3. File Impact Analysis

| File | Change Type | Purpose |
|---|---|---|
| `src/web/js/excel_block_renderer.js` | **New** | Pure frontend matrix calculation algorithm and HTML table generator. |
| `src/web/js/i18n.js` | **Modify** | Add Ukrainian and English localization keys for view mode controls and sidebar collapse buttons. |
| `src/web/index.html` | **Modify** | Add `#viewModeSwitcher`, `#excelBlockView`, `#btnToggleSidebarCollapse`, and `.sidebar-collapsed-strip`. |
| `src/web/css/style.css` | **Modify** | Dark theme styling for segmented view switcher, block matrix, and `.sidebar-collapsed` state. |
| `src/web/js/app.js` | **Modify** | Wire view mode switching, sidebar collapse controller, `localStorage` persistence, and dual rendering. |
| `tests/unit/test_frontend_contracts.py` | **New** | Automated contract tests validating JS methods, DOM IDs, and i18n parity. |
| `.specify/system_map.md` | **Modify** | Document `ExcelBlockRenderer`, dual-mode workspace, and collapsible sidebar. |
