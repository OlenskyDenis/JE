# Implementation Plan: Unified Tabbed Sidebar & Draggable Left-Edge Resizing

**Branch**: `013-unified-sidebar-tabs-resize` | **Date**: 2026-08-14 | **Spec**: [specs/013-unified-sidebar-tabs-resize/spec.md](spec.md)

**Input**: Feature specification from `/specs/013-unified-sidebar-tabs-resize/spec.md`

---

## Summary

Consolidate the existing 3-column UI layout into a 2-column layout by combining the **Excel Header Catalog** and **Leaf Node Absolute Paths** into a single right-hand tabbed sidebar panel with instant view toggling and live dual-badge counters. Equip this unified sidebar with a draggable vertical left-edge splitter/handle for real-time width resizing, clamped boundary constraints, double-click reset to 340px, and `localStorage` persistence.

---

## Technical Context

**Language/Version**: Python 3.14 (Backend RPC), Vanilla JavaScript / HTML5 / CSS3 (Frontend UI)  
**Frameworks/Libraries**: Eel (WebSocket RPC), openpyxl (Streaming Excel Engine)  
**Testing**: `pytest` test suite (`tests/unit/*`, `tests/integration/test_eel_bridge.py`)  
**Target Platform**: Desktop GUI (Windows / Chromium-based browser via Eel)  
**Constraints**: 100% backwards compatibility with existing DOM element IDs, non-destructive drag-and-drop, Row 1 Excel horizontal export, and zero backend regression.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan completed prior to implementation.
- **Principle II (Modular UI & OOP)**: PASSED. Tab and Resize controllers cleanly encapsulated in `app.js` without polluting global scope or breaking `TreeRenderer` / `DragDropHandler`.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md); preserved all critical DOM selectors (`#pathList`, `#pathCountBadge`, `#headerCountBadge`, `#sidebarHeaderList`, `#sheetSelector`, `#sidebarSearch`).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Handled boundary clamping, rapid tab toggling, pointer capture window leave, zero-data states, and DOM preservation for Excel export.

---

## Project Structure

### Documentation (this feature)

```text
specs/013-unified-sidebar-tabs-resize/
├── spec.md              # Feature specification (Clarified & Aligned)
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & event handling design
├── quickstart.md        # Manual and automated verification guide
└── checklists/
    └── requirements.md  # Quality and compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # Untouched (Cleanly decoupled backend RPC)
└── web/
    ├── index.html           # Replace 3 panels with 2 columns, Tab Bar, #sidebarResizer
    ├── css/
    │   └── style.css        # 2-column layout, tab styles, resizer handle, body.is-resizing
    └── js/
        ├── app.js           # Tab switching, pointer resize controller, localStorage sync
        ├── tree_renderer.js # Unchanged (renders to #pathList and #pathCountBadge)
        └── drag_drop.js     # Unchanged (binds to #sidebarHeaderList items seamlessly)
```

---

## Implementation Sequence

### Phase 1: HTML Structure Consolidation (`src/web/index.html`)
1. In `src/web/index.html`:
   - Replace the 3-panel `<main class="workspace-main three-column-layout">` with a 2-panel `<main class="workspace-main">`.
   - Preserve `.tree-panel` on the left.
   - Replace separate `.path-panel` and `.sidebar-panel` with `<section class="panel unified-sidebar-panel" id="unifiedSidebar">`.
   - Add `<div class="resizer-handle-left" id="sidebarResizer" title="Drag to resize sidebar (Double-click to reset)"></div>`.
   - Add Tab Bar `<div class="sidebar-tab-header">` with `#tabBtnCatalog` and `#tabBtnPaths`, each displaying its respective icon, label, and live badge count (`#headerCountBadge` and `#pathCountBadge`).
   - Wrap existing catalog controls and list in `<div class="sidebar-tab-content active" id="tabContentCatalog">`.
   - Wrap existing path list in `<div class="sidebar-tab-content hidden" id="tabContentPaths">`.

### Phase 2: CSS Styles for 2-Column Layout, Tabs & Resizer (`src/web/css/style.css`)
1. In `src/web/css/style.css`:
   - Update `.workspace-main` to `display: flex; flex-direction: row; gap: 16px; overflow: hidden;`.
   - Set `.tree-panel` to `flex: 1 1 0%; min-width: 320px;`.
   - Define `.unified-sidebar-panel` with `width: var(--sidebar-width, 340px); min-width: 260px; flex-shrink: 0; position: relative;`.
   - Style `.resizer-handle-left` with hover accent highlight (`--color-primary`) and `cursor: col-resize`.
   - Style `.sidebar-tab-header`, `.sidebar-tab-btn`, `.sidebar-tab-btn.active`, and `.sidebar-tab-content`.
   - Add `body.is-resizing` global styling to guarantee smooth pointer tracking and prevent text selection.

### Phase 3: JavaScript Controller Integration (`src/web/js/app.js`)
1. In `src/web/js/app.js`:
   - Add tab switching event listeners: toggle `.active` on tab buttons and `.hidden` on tab contents. Default to `catalog`.
   - Add pointer-based resizing logic on `#sidebarResizer`:
     - Calculate new width on `pointermove` based on distance from right window edge.
     - Clamp width between `260px` and `Math.min(window.innerWidth * 0.7, window.innerWidth - 320)`.
     - Update CSS variable `--sidebar-width` or style width.
     - Save to `localStorage.setItem('app_sidebar_width', width)` on `pointerup`.
     - Restore saved width from `localStorage` on `App.init()`.
     - Add `dblclick` listener on `#sidebarResizer` to reset width to `340px`.
   - Verify `handleExportReorganizedRow1` continues reading `.path-card` elements correctly from `#pathList`.

### Phase 4: System Map Sync & Verification
1. Update `.specify/system_map.md` to document the 2-column layout and unified tabbed sidebar.
2. Run automated test suite: `python -m pytest`.
3. Perform end-to-end manual verification in the Eel GUI (tab switching, resizing, catalog search, DnD into tree, Excel export).

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| DOM Compatibility | Low | All existing IDs retained in DOM; no broken querySelectors |
| Drag & Drop Conflict | Low | Resizer uses pointer events with capture; drag_drop.js handles HTML5 drag events |
| Excel Export Sync | Low | `#pathList` kept in DOM inside hidden tab container; querySelectorAll works reliably |
