# Implementation Plan: Tree Folder Collapse & Expand

**Branch**: `011-tree-folder-collapse-expand` | **Date**: 2026-08-14 | **Spec**: [specs/011-tree-folder-collapse-expand/spec.md](spec.md)

**Input**: Feature specification from `/specs/011-tree-folder-collapse-expand/spec.md`

---

## Summary

Implement client-side fold and unfold (collapse/expand) mechanics for folder-type elements in the Hierarchy Constructor Workspace, featuring interactive animated chevron toggles, pixel-perfect leaf indentation spacers, collapse state preservation across re-renders via `collapsedNodeIds` Set, auto-expansion on `NEST_CHILD` drops, and global "Expand All" / "Collapse All" toolbar buttons.

---

## Technical Context

**Language/Version**: HTML5 / Vanilla JS / CSS  
**Testing**: `pytest` (Regression suite)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Constraints**: Purely frontend visual enhancement; zero alterations to backend path generation or Excel Row 1 exports  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, and quickstart produced prior to implementation.
- **Principle II (OOP & SOLID)**: PASSED. Encapsulates tree folding state in `tree_renderer.js` and `app.js` without polluting core domain models.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md); builds directly onto `tree_renderer.js` and `app.js`.
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Verified that collapsing/expanding folders does not affect leaf path calculations or empty state behavior.

---

## Project Structure

### Documentation (this feature)

```text
specs/011-tree-folder-collapse-expand/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & state design
├── quickstart.md        # Verification workflow
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
└── web/
    ├── index.html       # Add #btnExpandAll and #btnCollapseAll in .panel-header of tree-panel
    ├── js/
    │   ├── tree_renderer.js # Render .node-toggle chevron on folders, .node-toggle-spacer on leaves, apply .collapsed
    │   ├── app.js       # Manage collapsedNodeIds Set, bind chevron click, expandAll, collapseAll, auto-expand on drop
    │   └── drag_drop.js # Support dropping onto collapsed nodes
    └── css/
        └── style.css    # .node-toggle, .chevron-icon rotation, .collapsed display rules, toolbar icon buttons
```

---

## Implementation Sequence

### Phase 1: HTML & CSS Styling (`index.html`, `style.css`)
1. In `src/web/index.html`:
   - Add `<div class="panel-header-actions">` inside `tree-panel` header containing `#btnExpandAll` and `#btnCollapseAll`.
2. In `src/web/css/style.css`:
   - Add styling for `.btn-icon-sm`, `.node-toggle`, `.chevron-icon`, `.node-toggle-spacer`.
   - Add `.tree-node.collapsed > .tree-node-content .chevron-icon { transform: rotate(-90deg); }`.
   - Add `.tree-node.collapsed > .tree-children { display: none; }`.

### Phase 2: Tree Renderer Updates (`tree_renderer.js`)
1. In `src/web/js/tree_renderer.js`:
   - Update `createNodeElement(node, collapsedNodeIds)`:
     - Check if `isFolder = Boolean(node.children && node.children.length > 0)`.
     - Check if `isCollapsed = collapsedNodeIds ? collapsedNodeIds.has(node.id) : false`.
     - Add `collapsed` class to `wrapper` if `isCollapsed`.
     - Render `<button class="node-toggle" data-id="${node.id}">` for folders and `<span class="node-toggle-spacer"></span>` for leaves.
   - Forward `collapsedNodeIds` recursively to child elements.

### Phase 3: Controller State & Event Binding (`app.js`)
1. In `src/web/js/app.js`:
   - Initialize `this.collapsedNodeIds = new Set()` in `init()`.
   - Bind click delegation for `.node-toggle` to toggle node ID in `collapsedNodeIds` and toggle `.collapsed` class on DOM node.
   - Implement `expandAll()` (clears `this.collapsedNodeIds` and re-renders) and `collapseAll()` (populates `this.collapsedNodeIds` and re-renders).
   - Bind `#btnExpandAll` and `#btnCollapseAll`.
   - In `onDropPayload`, when `zone === 'NEST_CHILD'`, delete `targetId` from `this.collapsedNodeIds`.
   - In `handleImportExcelFile` and `handleSwitchSheet`, clear `this.collapsedNodeIds`.

### Phase 4: System Map Update & Regression Validation
1. Update `.specify/system_map.md` with new toolbar controls and collapse capability.
2. Run `python -m pytest` to confirm 100% test pass rate across all 46 tests.

---

## Complexity Tracking

Zero architectural complexity. Pure visual and usability enhancement with clean state preservation.
