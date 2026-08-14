# Implementation Plan: Unified Drag-and-Drop Interaction Handler

## Architecture & Design Overview

The goal of this refactoring is to bring strict SOLID and DRY compliance to the drag-and-drop subsystem in the Database Hierarchy Creator web application.

Currently:
1. `DragDropHandler` in `src/web/js/drag_drop.js` maintains separate state properties `draggedNodeId` and `draggedSidebarHeader`.
2. `handleDrop` branches on `draggedSidebarHeader` and calls `onAddHeaderNode(parentId, headerLabel)` which passes only `parentId` and discards `activeDropZone`.
3. Consequently, catalog headers cannot be inserted as siblings (`BEFORE_SIBLING` / `AFTER_SIBLING`) above or below target nodes, and dropping onto a leaf node fails.

### Proposed Architecture

1. **Unified Drag Payload (`DragPayload`)**:
   - `isNew`: `true` for catalog headers, `false` for internal workspace tree nodes.
   - `id`: workspace node ID (for `isNew == false`).
   - `label`: header label text (for `isNew == true`).
   - `isContainer`: boolean (default `false` for catalog headers).

2. **Unified Controller (`DragDropHandler`)**:
   - Holds single active state: `activeDragPayload`, `activeDropTarget`, `activeDropZone`.
   - `handleDragOver`: Runs identical Y-coordinate 3-zone hit testing (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) and CSS highlighting regardless of payload source. Cycle check is performed when `isNew == false`.
   - `handleDrop`: Extracts `activeDragPayload` and target position `(targetId, zone)`. Invokes unified callback `onDropPayload(payload, targetId, zone)`.
   - `handleDragEnd`: Resets all drag state, highlights, and prohibition CSS classes.

3. **Backend Service & RPC Bridge (`WorkspaceForest`, `eel_bridge.py`)**:
   - Extend `WorkspaceForest.add_node_at_zone(node, target_node_id=None, zone=None)` to handle positioning new nodes relative to existing target nodes using `BEFORE_SIBLING`, `AFTER_SIBLING`, and `NEST_CHILD`.
   - Update `eel_bridge.py`'s `@eel.expose def add_node` signature and implementation to accept optional `target_id` and `zone` parameters.
   - Update `app.js` to dispatch catalog header drops through `eel.add_node(null, label, isContainer, targetId, zone)`.

## Impacted Files

- `src/hierarchy_lib/services/forest.py`: Add `add_node_at_zone` helper / update `move_node` and node insertion logic.
- `src/app/eel_bridge.py`: Update `add_node` RPC bridge method to accept `target_id` and `zone`.
- `src/web/js/drag_drop.js`: Refactor to unified `activeDragPayload`, unified hit testing, unified drop handler, and DRY event bindings.
- `src/web/js/app.js`: Connect unified drop callback to `eel.add_node` / `eel.move_node`.
- `tests/unit/test_forest.py` (or existing tests): Add unit tests verifying `add_node_at_zone` positioning for `BEFORE_SIBLING`, `AFTER_SIBLING`, and `NEST_CHILD`.
- `tests/integration/test_eel_bridge.py`: Add integration test verifying RPC `add_node` with `target_id` and `zone`.

## Verification Strategy

1. **Python Unit & Integration Tests**:
   - Run `python -m pytest` to verify backend tree manipulation with `target_id` and `zone`.
2. **Frontend UI Verification**:
   - Verify drag-and-drop interaction in browser environment / Eel bridge.
