# Research & Architectural Decisions: Move Active Workspace Sheet Selector to Canvas Workspace

**Feature**: 017-move-active-sheet-selector-to-canvas-workspace  
**Date**: 2026-08-14  

---

## Decision 1: Inline Placement in Canvas Header Group

- **Context**: In previous versions, the Active Workspace Sheet selector was located in the right sidebar alongside the catalog selector. This created cognitive friction and took up vertical space in the sidebar.
- **Decision**: Embed the selector directly in the left workspace header `.panel-header .panel-title-group` as an inline control: `Sheet: [Sales ▾]`.
- **Rationale**:
  1. **Direct Manipulation**: Connects the workspace canvas with the sheet it represents directly in the visual field of view.
  2. **Maximized Vertical Space**: Replaces the static badge without adding extra toolbar rows.
  3. **Dedicated Sidebar**: The sidebar becomes 100% focused on header discovery, search, and drag-and-drop catalog operations.

---

## Decision 2: Styling and Compact Responsive Design

- **Decision**:
  - Container `.workspace-sheet-picker`: subtle blue accent background (`rgba(59, 130, 246, 0.12)`), 1px border (`rgba(59, 130, 246, 0.3)`), border-radius 8px.
  - Label `.workspace-sheet-label`: small uppercase text `SHEET:`.
  - Select `.workspace-sheet-select`: transparent borderless select with `max-width: 180px` and text ellipsis for long sheet names.
- **Rationale**: Blends naturally into the dark theme design system alongside the node count badge.
