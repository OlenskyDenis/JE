# Implementation Plan: Unique Level Hierarchy View (Level-by-Level Unique Headers & Cross-Level Highlighting)

**Feature Branch**: `028-unique-level-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  
**Spec**: [specs/028-unique-level-hierarchy-view/spec.md](spec.md)  
**Research**: [specs/028-unique-level-hierarchy-view/research.md](research.md)  
**Data Model**: [specs/028-unique-level-hierarchy-view/data-model.md](data-model.md)  
**Quickstart**: [specs/028-unique-level-hierarchy-view/quickstart.md](quickstart.md)  

---

## 1. Architecture Overview

This feature introduces a 3rd workspace inspection mode (**Unique Level Hierarchy View**) which decomposes active tree hierarchies into horizontal stacked level rows containing deduplicated unique header terms. It detects terms repeated across different depths (case-insensitive cross-level matches), decorates them with badges, and provides synchronized interactive hover highlights across all levels.

---

## 2. Implementation Phases

### Phase 1: Baseline Verification
- Run existing automated test suite (`python -m pytest`) to ensure a clean 80-test baseline.

### Phase 2: Core Level Deduplication & Match Engine (`src/web/js/unique_level_renderer.js`)
- Implement `UniqueLevelRenderer` object:
  - `extractUniqueLevels(roots)`: Computes `levelMaps` and `termLevelsMap` using case-insensitive normalization.
  - `renderUniqueLevels(roots, containerEl)`: Generates semantic HTML layout with stacked `.level-row-container`, `.level-row-header` (level title, unique count, match count), `.level-chips-container`, and `.level-header-chip` elements.
  - Generates rich hover tooltips and cross-level match badges (`[Збіг: Рівні X, Y]`).
  - Implements event delegation on container for synchronized hover highlighting (`.highlight-match-sync`).

### Phase 3: Localization & Internationalization (`src/web/js/i18n.js`)
- Register Ukrainian (`uk`) and English (`en`) dictionary keys for:
  - `view_mode_unique_levels`, `tooltip_view_mode_unique_levels`
  - `level_roots_title`, `level_tier_title`
  - `level_unique_stat`, `level_match_stat`
  - `chip_match_badge`
  - `unique_levels_empty_title`, `unique_levels_empty_hint`

### Phase 4: HTML Markup & Dark Theme Styling
- Update [`src/web/index.html`](file:///E:/JE/src/web/index.html):
  - In `#viewModeSwitcher`: add `#btnViewUniqueLevels` button.
  - In `#treeContainer`: add `<div id="uniqueLevelView" class="unique-level-view hidden"></div>`.
  - Include `<script src="js/unique_level_renderer.js"></script>`.
- Update [`src/web/css/style.css`](file:///E:/JE/src/web/css/style.css):
  - Add dark theme styling for `.unique-level-view`, `.level-row-container`, `.level-row-header`, `.level-chips-container`, `.level-header-chip`, `.has-cross-match`, and `.highlight-match-sync`.

### Phase 5: App Controller Wiring & State Synchronization (`src/web/js/app.js`)
- In `App.bindDOM()`: Bind `#btnViewUniqueLevels` and `#uniqueLevelView`.
- In `App.bindEvents()`: Wire click listener for `this.switchViewMode('unique_levels')`.
- In `App.switchViewMode(mode)`: Support 3 modes (`tree`, `matrix`, `unique_levels`), manage active button classes, toggle container visibility, and call `UniqueLevelRenderer.renderUniqueLevels(this.currentRoots, this.uniqueLevelViewEl)`.
- In `App.updateUI(roots)`: Trigger `UniqueLevelRenderer.renderUniqueLevels(roots, this.uniqueLevelViewEl)`.

### Phase 6: System Map, Contract Tests & Verification
- Update `.specify/system_map.md` with `UniqueLevelRenderer` and 3-mode workspace view support.
- Run `python -m pytest` including `tests/unit/test_frontend_contracts.py` ensuring 100% pass rate.

### Phase 7: Double-Click Editing in Excel Blocks & Unique Level Views (Quick Fix)
- Add `tooltip_dblclick_edit` dictionary key in `src/web/js/i18n.js` (`"(Подвійний клік для редагування)"` / `"(Double-click to edit)"`).
- Update `ExcelBlockRenderer` to attach `data-node-id`, `data-node-name`, `data-data-type`, `data-is-folder` to `.matrix-cell` and append the edit hint to cell tooltips.
- Update `UniqueLevelRenderer` to attach `data-node-id`, `data-node-name`, `data-data-type`, `data-is-folder` to `.level-header-chip` and append the edit hint to chip tooltips.
- Update `App.bindEvents()` in `src/web/js/app.js` with `dblclick` event delegation on `#excelBlockView` and `#uniqueLevelView` invoking `openEditModal`.
- Update `src/web/css/style.css` with `cursor: pointer` for `.matrix-cell` and `.level-header-chip`.
- Run `python -m pytest` to ensure complete contract test validation.

### Phase 8: Batch Editing with Notification in Unique Level View (Quick Fix)
- Add `modal_batch_edit_notice` and `toast_batch_nodes_updated` dictionary keys in `src/web/js/i18n.js`.
- Add `#modalBatchNotice` alert box with `#modalBatchNoticeText` inside `#nodeModal` in `src/web/index.html`.
- Style `.modal-batch-notice` in `src/web/css/style.css` with amber warning styling and SVG icon.
- Enhance `openEditModal()` in `src/web/js/app.js` to accept `batchMeta = { count, nodeIds, level }`, render the notice dynamically, and update all nodes on that level in `submitModal()`.
- Validate via `python -m pytest`.

---

## 3. File Impact Analysis

| File | Change Type | Purpose |
|---|---|---|
| `src/web/js/unique_level_renderer.js` | **New** | Pure frontend level extraction, deduplication, match calculation, and rendering. |
| `src/web/js/i18n.js` | **Modify** | Add dictionary translations for level titles, match stats, and empty states. |
| `src/web/index.html` | **Modify** | Add `#btnViewUniqueLevels`, `#uniqueLevelView` container, and load script. |
| `src/web/css/style.css` | **Modify** | Add styles for level rows, chips, cross-match badges, and hover sync highlights. |
| `src/web/js/app.js` | **Modify** | Wire 3-way view mode switching, `localStorage` persistence, and state sync. |
| `.specify/system_map.md` | **Modify** | Document `UniqueLevelRenderer` module. |
