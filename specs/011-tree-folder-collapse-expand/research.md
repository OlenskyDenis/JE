# Research & Architectural Decisions: Tree Folder Collapse & Expand

**Feature**: 011-tree-folder-collapse-expand  
**Date**: 2026-08-14  

## Decision 1: Client-Side State Encapsulation via `collapsedNodeIds` Set

- **Context**: Users can toggle folder folding/unfolding manually. When the tree re-renders following Eel RPC operations (adding child, moving, renaming), the user's manual folding state must be preserved.
- **Decision**:
  - Maintain `this.collapsedNodeIds = new Set()` in `App` controller (`src/web/js/app.js`).
  - Pass `this.collapsedNodeIds` to `TreeRenderer.renderTree(roots, containerEl, collapsedNodeIds)`.
  - Toggling a folder adds/removes its `node.id` in `this.collapsedNodeIds` and toggles `.collapsed` class on the `.tree-node` element.
  - Reset `this.collapsedNodeIds.clear()` when opening a new Excel file or switching sheets so trees default to fully expanded.
- **Rationale**: Clean, lightweight client-side state without cluttering backend domain models or payload serialization.

## Decision 2: Chevron DOM Layout & Alignment Spacer

- **Context**: Folders have children to collapse, whereas leaf nodes do not. If chevrons are rendered only on folders without alignment spacing for leaves, child nodes under folders would be visually misaligned.
- **Decision**:
  - Render an interactive `<button class="node-toggle" data-id="${node.id}">` containing an SVG chevron for nodes where `children.length > 0`.
  - Render a `<span class="node-toggle-spacer"></span>` with identical width (20px) for leaf nodes (`children.length === 0`).
  - Style chevron icon with CSS rotation: `transform: rotate(0deg)` when expanded (pointing down), and `transform: rotate(-90deg)` when collapsed (pointing right).
- **Rationale**: Ensures pixel-perfect vertical alignment and standard hierarchical tree ergonomics.

## Decision 3: Global Toolbar Controls (Expand All / Collapse All)

- **Context**: In large enterprise spreadsheets with hundreds of columns and deep multi-level categories, manual 1-by-1 folding can be tedious.
- **Decision**:
  - Add `#btnExpandAll` and `#btnCollapseAll` to the `.panel-header` of the tree panel.
  - `expandAll()` clears `this.collapsedNodeIds` and re-renders.
  - `collapseAll()` collects all node IDs with `children.length > 0` into `this.collapsedNodeIds` and re-renders.
- **Rationale**: Provides instant 1-click tree management for high-density database hierarchies.

## Decision 4: Auto-Expansion on `NEST_CHILD` Drops

- **Context**: If a folder is collapsed and a user drops a new child into it (`NEST_CHILD`), the user needs immediate visual confirmation that the drop succeeded.
- **Decision**:
  - When a drop with `zone === 'NEST_CHILD'` succeeds on `targetId`, delete `targetId` from `this.collapsedNodeIds`.
- **Rationale**: Prevents confusion where newly added children appear to "disappear" into a closed folder.
