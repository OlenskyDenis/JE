# Implementation Plan: In-Place / Modal Node Renaming in Workspace

**Branch**: `019-node-renaming-in-workspace` | **Date**: 2026-08-14 | **Spec**: [specs/019-node-renaming-in-workspace/spec.md](spec.md)

**Input**: Feature specification from `/specs/019-node-renaming-in-workspace/spec.md`

---

## Summary

Implement node renaming across the entire application stack: `HierarchyNode.rename` in domain models, `rename_node(node_id, new_name)` in the Eel RPC bridge, a pencil action button (`.btn-node-edit`) on each node card in `TreeRenderer`, and double-click triggers on `.node-label` in `app.js`. The edit modal (`#nodeModal`) pre-populates with current name, autofocused and selected, automatically recalculating leaf paths and setting `isDirty = true`.

---

## Technical Context

**Language/Version**: Python 3.14 (Core Domain & RPC), Vanilla JavaScript ES6+, HTML5, CSS3  
**Testing**: `pytest` test suite (`tests/unit/test_composite.py`, `tests/integration/test_eel_bridge.py`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 100% path cascade consistency, 0 regression in drag-and-drop or expand/collapse operations, non-empty name validation.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan authored prior to code changes.
- **Principle II (OOP & Clean State Architecture)**: PASSED. `HierarchyNode.rename` handles validation at the domain level; RPC bridge cleanly updates session state.
- **Principle IV (Library-First & TDD)**: PASSED. Unit tests in `test_composite.py` and RPC tests in `test_eel_bridge.py` specified first.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Validated whitespace trimming, special characters, deep folder path propagation, and modal keyboard handling (`Enter`/`Escape`).

---

## Project Structure

### Documentation (this feature)

```text
specs/019-node-renaming-in-workspace/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & UI interaction model
├── quickstart.md        # Verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
├── app/
│   └── eel_bridge.py        # @eel.expose def rename_node(node_id, new_name)
├── hierarchy_lib/
│   └── models/
│       └── composite.py     # HierarchyNode.rename(new_name) with validation
└── web/
    └── js/
        ├── app.js           # openEditModal, modalMode branching, dblclick & click listeners
        └── tree_renderer.js # .btn-node-edit pencil icon in .node-actions
```

---

## Implementation Sequence

### Phase 1: Core Domain Model & TDD Unit Tests (`src/hierarchy_lib/`)
1. In `src/hierarchy_lib/models/composite.py`: Add `HierarchyNode.rename(new_name)` with whitespace trimming and non-empty validation.
2. In `tests/unit/test_composite.py`: Add unit tests for node renaming, whitespace trimming, and empty-string rejection.

### Phase 2: Backend Eel RPC Bridge & Integration Tests (`src/app/`)
1. In `src/app/eel_bridge.py`: Add `@eel.expose def rename_node(node_id: str, new_name: str) -> Dict[str, Any]`.
2. In `tests/integration/test_eel_bridge.py`: Add integration test verifying `rename_node` endpoint and leaf path regeneration.

### Phase 3: Frontend Tree Renderer & Controller Interaction (`src/web/js/`)
1. In `src/web/js/tree_renderer.js`: Add `.btn-node-edit` with SVG pencil icon in `renderNode`.
2. In `src/web/js/app.js`:
   - Introduce `modalMode: 'create' | 'edit'` and `openEditModal(nodeId, currentName)`.
   - Update `handleModalSubmit()` to call `eel.rename_node` when in `'edit'` mode.
   - Attach click listener for `.btn-node-edit` and `dblclick` listener for `.node-label`.
   - Ensure `isDirty = true` on rename and trigger UI/path re-render.

### Phase 4: System Map Sync & Quality Assurance
1. Update [`.specify/system_map.md`](../../.specify/system_map.md).
2. Run full pytest suite `python -m pytest` (48+ tests).
3. Execute end-to-end manual verification per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| Domain Validation | Negligible | Pure Python method with standard ValueError |
| Event Delegation | Low | Handled via existing treeView container listeners |
| Path Recalculation | Negligible | `PathGenerator.calculate_all_paths` runs over existing object references |
