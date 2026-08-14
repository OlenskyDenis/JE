# Research & Architectural Decisions: Unified Tabbed Sidebar & Draggable Left-Edge Resizing

**Feature**: 013-unified-sidebar-tabs-resize  
**Date**: 2026-08-14  

---

## Decision 1: 2-Column Flexbox Layout over CSS Grid

- **Context**: The existing workspace used CSS grid `.workspace-main.three-column-layout { grid-template-columns: 1fr 280px 300px; }`.
- **Decision**: Transition `.workspace-main` to a Flexbox layout:
  - Tree workspace: `flex: 1 1 0%; min-width: 320px;`
  - Unified Sidebar: `width: var(--sidebar-width, 340px); min-width: 260px; max-width: 70vw; flex-shrink: 0; position: relative;`
- **Rationale**: Flexbox allows direct real-time manipulation of the sidebar width via pixel values (`--sidebar-width` or `element.style.width`) with instant, fluid adjustment of the tree canvas width without needing dynamic grid-template recalculation.

---

## Decision 2: Pointer Events with Global Capture for Resizing

- **Context**: Left-edge dragging requires smooth tracking across fast cursor movements, boundary hits, and outside the application window.
- **Decision**:
  - Attach `pointerdown` to the `#sidebarResizer` element.
  - Call `e.target.setPointerCapture(e.pointerId)` or add `pointermove` and `pointerup` listeners to `window`.
  - Add `is-resizing` class to `document.body` during drag to enforce `cursor: col-resize` and `user-select: none`.
  - On `pointerup`, remove listeners/classes and write the final width to `localStorage.setItem('app_sidebar_width', width)`.
- **Rationale**: Pointer Events API unified across mouse and touch, eliminates cursor flickering, and guarantees clean drag termination even if the mouse leaves the browser window.

---

## Decision 3: DOM Visibility Toggling for Tabs (`display: none` / `.hidden`)

- **Context**: `App.handleExportReorganizedRow1` reads `.path-card` elements from `#pathList` in the DOM (`this.pathListEl.querySelectorAll('.path-card')`).
- **Decision**: Keep both view containers (`#tabContentCatalog` and `#tabContentPaths`) mounted in the DOM at all times. Use CSS `.hidden` (`display: none !important`) to toggle visibility.
- **Rationale**:
  - `querySelectorAll('.path-card')` will find all rendered leaf path cards regardless of which tab is active, enabling Excel export from any tab without DOM re-renders.
  - Zero latency when toggling between tabs.
  - Preserves user search text and scroll position in the inactive tab.

---

## Decision 4: Live Dual-Badge Display on Tab Bar

- **Context**: Users benefit from knowing the count of available Excel headers and generated leaf paths at a glance.
- **Decision**: Place `#headerCountBadge` inside `#tabBtnCatalog` and `#pathCountBadge` inside `#tabBtnPaths`. Update both badges on every workspace refresh or Excel import.
- **Rationale**: High-information-density UI without clutter; provides live status of both data streams concurrently.

---

## Decision 5: Boundary Constraints and Double-Click Reset

- **Context**: Accidental drags could collapse the sidebar to 0px or crush the tree canvas.
- **Decision**:
  - Minimum width: `260px`
  - Maximum width: `Math.min(window.innerWidth * 0.7, window.innerWidth - 320)` (guarantees at least 320px for tree canvas).
  - Double-click on `#sidebarResizer` resets width to `340px`.
- **Rationale**: Prevents unusable layout states and provides a fast recovery shortcut.
