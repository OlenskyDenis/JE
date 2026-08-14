# Implementation Plan: Dynamic HierarchyNode Unification

**Branch**: `008-dynamic-node-unification` | **Date**: 2026-08-14 | **Spec**: [specs/008-dynamic-node-unification/spec.md](spec.md)

**Input**: Feature specification from `/specs/008-dynamic-node-unification/spec.md` and user technical directive:
"Refactor the Composite tree model: use a single 'HierarchyNode' class with a dynamic 'is_folder' property. Update the drag-and-drop controller to support dropping payload inside any node, automatically appending it to the 'children' array of that node and updating the UI dynamically."

---

## Summary

Unify `CompositeNode` and `LeafNode` into a single `HierarchyNode` class across the domain model, services, bridge, and frontend renderer. State is evaluated dynamically: a node with `len(children) > 0` is a folder/container (`is_folder = True`, `is_container = True`), and a node with `len(children) == 0` is a leaf (`is_folder = False`, `is_container = False`). Adding a child to any node upgrades it to a folder, and removing its last child downgrades it to a leaf. Update drag-and-drop to universally permit `NEST_CHILD` drops on any node.

---

## Technical Context

**Language/Version**: Python 3.14 / HTML5 + Vanilla JS (Eel UI)  
**Primary Dependencies**: `eel`, `openpyxl`, `pytest`  
**Storage**: Native Excel `.xlsx` files  
**Testing**: `pytest` (Unit & Integration tests)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Performance Goals**: <16ms dynamic state transition & re-render on child addition/removal  
**Constraints**: Maintain full backward compatibility for serialized DTOs (`is_container`, `children`, `absolute_path`)  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec, plan, research, data model, contracts, and quickstart produced prior to implementation.
- **Principle II (OOP & SOLID)**: PASSED. Eliminates rigid type coupling with cohesive `HierarchyNode` design.
- **Principle III (GoF Composite Pattern)**: PASSED. Dynamic Composite pattern implemented cleanly with uniform component interface.
- **Principle IV (Library-First & TDD)**: PASSED. Core domain unit tests updated and verified before UI wiring.
- **Principle V (Self-Contained Excel)**: PASSED. Excel import and export continue to use `openpyxl`.

---

## Project Structure

### Documentation (this feature)

```text
specs/008-dynamic-node-unification/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Architectural decisions & dynamic transitions
├── data-model.md        # Unified HierarchyNode class & DTO schema
├── quickstart.md        # Manual and automated verification guide
├── contracts/
│   └── hierarchy_node.json # Dynamic DTO contract
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
├── hierarchy_lib/
│   ├── models/
│   │   ├── base.py            # Base component interface
│   │   ├── node.py            # NEW: Unified HierarchyNode class (with is_folder dynamic property)
│   │   ├── composite.py       # CompositeNode alias / wrapper for backwards compatibility
│   │   └── leaf.py            # LeafNode alias / wrapper for backwards compatibility
│   └── services/
│       ├── forest.py          # Universal WorkspaceForest supporting NEST_CHILD on any node
│       ├── path_parser.py     # Uses HierarchyNode for tree construction
│       └── path_generator.py  # Checks len(children) == 0 for leaf paths
├── app/
│   └── eel_bridge.py          # Instantiates HierarchyNode in RPC endpoints
└── web/
    └── js/
        ├── tree_renderer.js   # Dynamic folder vs leaf visual rendering & universal '+ Add Child'
        ├── drag_drop.js       # Universal NEST_CHILD drag & drop
        └── app.js             # Simplified node creation

tests/
├── unit/
│   ├── test_composite.py      # Unit tests for HierarchyNode dynamic state transitions
│   ├── test_forest_zone_addition.py # Unit tests for zone addition & universal nesting
│   ├── test_path_parser.py    # Unit tests for path parser
│   └── test_excel_adapter.py  # Unit tests for adapter
└── integration/
    └── test_eel_bridge.py     # Integration tests for Eel endpoints
```

---

## Implementation Sequence

### Phase 1: Core Domain Model (`HierarchyNode`) (TDD)
1. Update `tests/unit/test_composite.py` to test:
   - Dynamic `is_folder` / `is_container` property (`len(children) > 0`).
   - Dynamic upgrade: adding a child to a 0-child node sets `is_folder = True`.
   - Dynamic downgrade: removing the last child sets `is_folder = False`.
   - Recursive finding, ancestor checking, and serialization.
2. Implement `src/hierarchy_lib/models/node.py` (`HierarchyNode`) and update `src/hierarchy_lib/models/composite.py` and `leaf.py`.

### Phase 2: Services Refactoring (`WorkspaceForest`, `PathParserService`)
1. In `src/hierarchy_lib/services/forest.py`:
   - Refactor `add_node_at_zone`: remove leaf node restriction on `NEST_CHILD` so any `HierarchyNode` can receive children.
   - Refactor `get_all_leaf_paths`: collect paths for all nodes with `len(children) == 0`.
2. In `src/hierarchy_lib/services/path_parser.py`:
   - Use `HierarchyNode` uniformly for all path segments.
3. In `src/app/eel_bridge.py`:
   - Use `HierarchyNode` in `add_node`.

### Phase 3: Frontend Web UI Refactoring (`tree_renderer.js`, `drag_drop.js`, `app.js`)
1. In `src/web/js/tree_renderer.js`:
   - Determine folder state dynamically: `const isFolder = node.children && node.children.length > 0;`.
   - Render folder icon vs leaf icon dynamically based on `isFolder`.
   - Add `+ Add Child` action button to ALL nodes.
2. In `src/web/js/drag_drop.js`:
   - Ensure all nodes accept `NEST_CHILD` drop zone.

### Phase 4: Polish & Full Test Execution
1. Run `python -m pytest` across all unit and integration tests.

---

## Complexity Tracking

Significantly reduces structural complexity and eliminates subclass hierarchies and runtime type checking errors.
