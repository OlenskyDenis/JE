# Implementation Plan: Database Hierarchy Creator with Excel Integration

**Branch**: `001-database-hierarchy-creator` | **Date**: 2026-08-13 | **Spec**: [`specs/001-database-hierarchy-creator/spec.md`](file:///E:/JE/specs/001-database-hierarchy-creator/spec.md)

**Input**: Feature specification from `/specs/001-database-hierarchy-creator/spec.md`

---

## Summary

Build a desktop Database Hierarchy Creator application compatible with Excel. The application features:
1. **Standalone Core Library (`hierarchy_lib`)**: Python 3.12 backend implementing the Gang of Four (GoF) Composite Object-Oriented design pattern (`HierarchyComponent`, `CompositeNode`, `LeafNode`) for modeling multi-root tree structures with infinite nesting depth, backslash-separated absolute path generation (`Root\Folder\Subfolder\Item`), and self-contained Excel `.xlsx` import/export processing using `openpyxl` (no MS Excel desktop installation required).
2. **Desktop UI Wrapper (`Eel`)**: Lightweight desktop wrapper using Python `Eel` hosting a responsive HTML5 / CSS3 / Vanilla JS frontend.
3. **Interactive Constructor UI**: Drag-and-drop constructor UI supporting **Three-Zone Target Detection** (top/bottom 25% for sibling reordering, center 50% for child nesting) and real-time cycle rejection (prohibited cursor, snap-back animation, and warning toast notification).

---

## Technical Context

- **Language/Version**: Python 3.12+
- **Primary Dependencies**:
  - `eel` (v0.16+): Desktop UI webview wrapper & Python-JS websocket RPC bridge
  - `openpyxl` (v3.1+): Self-contained OpenXML spreadsheet reader/writer
- **Storage**: In-memory Composite object graph with `.xlsx` import/export file persistence
- **Testing**: `pytest` (v8.0+) for unit and contract testing of the core library and Excel adapters
- **Target Platform**: Desktop (Windows / macOS / Linux cross-platform)
- **Project Type**: Desktop Application + Standalone Python Library
- **Performance Goals**: Absolute path calculation for 10,000 nodes in <300ms; drag-and-drop zone detection and DOM updates in <50ms
- **Constraints**: 100% self-contained Excel processing without Microsoft Excel desktop or COM interop dependencies; strict SDD phase scope enforcement (no source code edits during plan phase)
- **Scale/Scope**: Infinite nesting depth, multi-root forest tree structures, workbooks with arbitrary worksheet counts

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle / Gate | Compliance Status | Implementation Strategy |
|---|---|---|
| **I. Spec-Driven Development (SDD)** | **PASS** | No source code (`.py`, `.html`, `.js`, `.css`) is created or edited during this plan phase. Only planning documents (`plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`) are produced. |
| **II. Object-Oriented Programming (OOP) & SOLID** | **PASS** | Domain model strictly designed with OOP inheritance (`HierarchyComponent` base) and SOLID principles (SRP, OCP, LSP, ISP, DIP). |
| **III. Gang of Four (GoF) Composite Pattern** | **PASS** | Tree nodes explicitly implement the Composite pattern (`CompositeNode` contains `HierarchyComponent` list; `LeafNode` represents terminal items). |
| **IV. Library-First Approach & TDD** | **PASS** | Core logic encapsulated in standalone package `src/hierarchy_lib/` independent of UI/Eel layers, fully tested using `pytest` prior to UI assembly. |
| **V. Self-Contained Excel Processing** | **PASS** | `openpyxl` library used for native `.xlsx` reading and writing without MS Excel desktop or COM interop dependencies. |

---

## Project Structure

### Documentation (this feature)

```text
specs/001-database-hierarchy-creator/
├── plan.md              # Main implementation plan
├── research.md          # Technical decisions & stack research
├── data-model.md        # Composite OOP classes & Excel data mapping schema
├── quickstart.md        # Environment setup, test execution, and run instructions
└── contracts/
    └── eel_bridge.json  # RPC schema contract between Python backend & Eel JS frontend
```

### Source Code Layout (Repository Root)

```text
src/
├── hierarchy_lib/              # Standalone Core Library (Library-First approach)
│   ├── __init__.py
│   ├── models/                 # GoF Composite Pattern Classes
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract HierarchyComponent base class
│   │   ├── composite.py        # CompositeNode (container) class
│   │   └── leaf.py             # LeafNode (terminal item) class
│   ├── services/               # Domain Logic & Path Services
│   │   ├── __init__.py
│   │   ├── path_generator.py   # Absolute path generator (Root\Folder\Item)
│   │   └── forest.py           # WorkspaceForest multi-root tree manager
│   └── adapters/               # Self-Contained Excel Adapters (openpyxl)
│       ├── __init__.py
│       └── excel_adapter.py    # Excel single-line sheet import & vertical segment export
│
├── app/                        # Eel Desktop Application & Bridge Layer
│   ├── __init__.py
│   ├── eel_bridge.py           # Eel @eel.expose RPC methods & DTO serializers
│   └── main.py                 # Application launcher (eel.init, eel.start)
│
└── web/                        # Responsive Drag-and-Drop Frontend UI
    ├── index.html              # Main workspace layout
    ├── css/
    │   ├── style.css           # Modern theme tokens & responsive tree layout
    │   └── drag_drop.css       # 3-zone drag targets & prohibited cursor styles
    └── js/
        ├── app.js              # Eel websocket bridge caller & state sync
        ├── tree_renderer.js    # DOM tree node renderer & path badge updates
        └── drag_drop.js        # Three-zone hit testing (top/bottom 25%, center 50%) & cycle validator

tests/
├── unit/                       # TDD Core Library Tests
│   ├── test_composite.py      # Unit tests for CompositeNode & LeafNode
│   ├── test_path_generator.py # Unit tests for path generation & multi-root trees
│   └── test_excel_adapter.py  # Unit tests for openpyxl import/export
│
└── integration/                # Desktop UI & Bridge Tests
    └── test_eel_bridge.py      # Contract tests for Eel RPC backend endpoints
```

**Structure Decision**: Selected isolated module structure separating standalone library (`src/hierarchy_lib/`), desktop wrapper (`src/app/`), frontend assets (`src/web/`), and pytest test suites (`tests/unit/`, `tests/integration/`).

---

## Complexity Tracking

> *No constitutional violations detected. Complexity remains low and strictly modular.*

| Component | Design Choice | Simpler Alternative Rejected Because |
|-----------|---------------|--------------------------------------|
| **Standalone Package** | `src/hierarchy_lib/` | Inline UI backend scripts violate Constitution Principle IV (Library-First & TDD). |
| **GoF Composite Pattern** | `HierarchyComponent` / `CompositeNode` / `LeafNode` | Untyped dictionary trees lack type safety, cycle validation methods, and SOLID compliance. |
| **Three-Zone Hit Testing** | Top/Bottom 25% (sibling), Center 50% (child) | Single drop target prevents clean visual sibling reordering in tree structures. |
