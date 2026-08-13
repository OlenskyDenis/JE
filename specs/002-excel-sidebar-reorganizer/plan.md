# Implementation Plan: Excel Header Reorganization & Database Structure Designer

**Branch**: `feature/excel-sidebar-reorganizer` | **Date**: 2026-08-13 | **Spec**: [specs/002-excel-sidebar-reorganizer/spec.md](spec.md)

**Input**: Feature specification from `/specs/002-excel-sidebar-reorganizer/spec.md`

---

## Summary

Build a sidebar-assisted Excel header reorganizer allowing users to import multi-sheet Excel workbooks, extract unique Row 1 headers per sheet, filter headers via real-time search in an alphabetical sidebar, non-destructively drag headers into a main tree editor, and export the resulting tree as horizontal Row 1 leaf path strings across columns under the original sheet name using `openpyxl`.

---

## Technical Context

**Language/Version**: Python 3.14 / HTML5 + Vanilla JS (Eel UI)  
**Primary Dependencies**: `openpyxl`, `eel`, `pytest`  
**Storage**: Native Excel `.xlsx` files  
**Testing**: `pytest` (Unit & Integration tests)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Project Type**: Desktop GUI Web Application (Eel Python + HTML/CSS/JS frontend)  
**Performance Goals**: <500ms sheet switching, <300ms header extraction (1k cells), <100ms real-time search filter  
**Constraints**: Zero Microsoft Excel installation requirement (`openpyxl` self-contained), non-destructive sidebar reuse  
**Scale/Scope**: Up to 50 sheet workbooks, up to 1,000 headers per sheet  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. No source code generated during specify/plan phases.
- **Principle II (OOP & SOLID)**: PASSED. Class interfaces follow SRP, OCP, LSP, ISP, DIP.
- **Principle III (GoF Composite Pattern)**: PASSED. Tree nodes implement Composite pattern (`TreeConstructorNode` / `CompositeNode`).
- **Principle IV (Library-First & TDD)**: PASSED. Extraction and export services isolated in standalone Python library modules with TDD prior to UI wiring.
- **Principle V (Self-Contained Excel)**: PASSED. Standard `openpyxl` file processing without COM / MS Excel application dependency.

---

## Project Structure

### Documentation (this feature)

```text
specs/002-excel-sidebar-reorganizer/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Phase 0 architectural decisions
├── data-model.md        # Phase 1 domain entities & schema
├── quickstart.md        # Phase 1 end-to-end validation guide
├── contracts/
│   └── eel_bridge.json  # Phase 1 Eel RPC API contract
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
├── app/
│   ├── eel_bridge.py          # Eel RPC endpoints for header extraction, sheet switching, and export
│   └── main.py                # App entry point initializing Eel
├── hierarchy_lib/
│   ├── adapters/
│   │   └── excel_adapter.py   # Row 1 header extraction & horizontal path export adapter
│   ├── models/
│   │   ├── base.py            # Base node interface
│   │   ├── composite.py       # Composite container node
│   │   └── leaf.py            # Leaf node
│   └── services/
│       ├── forest.py          # Multi-root tree manager
│       ├── header_service.py  # Header extraction, deduplication & sorting service
│       └── path_generator.py  # Leaf path calculator
└── web/
    ├── css/
    │   ├── drag_drop.css      # Non-destructive drag-and-drop styles
    │   └── style.css          # Main UI layout & sidebar styles
    ├── index.html             # UI with sidebar & main canvas
    └── js/
        ├── app.js             # Eel bridge interaction & sheet selector state
        ├── drag_drop.js       # Non-destructive HTML5 drag & drop handler
        └── tree_renderer.js   # Tree builder canvas UI renderer

tests/
├── integration/
│   └── test_eel_bridge.py     # Integration tests for Eel backend endpoints
└── unit/
    ├── test_excel_adapter.py  # Unit tests for horizontal Row 1 import & export
    ├── test_header_service.py # Unit tests for header extraction, deduplication & sorting
    └── test_path_generator.py # Unit tests for path generator
```

**Structure Decision**: Single Python project structure with modular decoupled `hierarchy_lib` backend package, Eel app wrapper, and web frontend UI directory.

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *All principles strictly satisfied without complexity violations.* | *N/A* |
