# Implementation Plan: Automatic Hierarchical Excel Header Import & Workspace Tree Generator

**Branch**: `006-excel-hierarchical-import` | **Date**: 2026-08-14 | **Spec**: [specs/006-excel-hierarchical-import/spec.md](spec.md)

**Input**: Feature specification from `/specs/006-excel-hierarchical-import/spec.md`

---

## Summary

Automatically parse Excel Row 1 headers formatted as backslash-delimited paths (`Root\Folder\Leaf`) upon file import or sheet switching and instantiate the hierarchical tree structure directly in the Hierarchy Constructor Workspace canvas. Intermediate path elements become nested `CompositeNode` folder containers (with common prefixes merged), terminal elements become `LeafNode` items, and single-segment headers become root nodes.

---

## Technical Context

**Language/Version**: Python 3.14 / HTML5 + Vanilla JS (Eel UI)  
**Primary Dependencies**: `openpyxl`, `eel`, `pytest`  
**Storage**: Native Excel `.xlsx` files  
**Testing**: `pytest` (Unit & Integration tests)  
**Target Platform**: Desktop (Windows / Chrome via Eel)  
**Project Type**: Desktop GUI Web Application (Eel Python + HTML/CSS/JS frontend)  
**Performance Goals**: <200ms automatic tree parsing and canvas rendering for workbooks up to 500 headers  
**Constraints**: Zero Microsoft Excel installation requirement (`openpyxl` self-contained), maintain existing drag-and-drop & export capabilities  
**Scale/Scope**: Up to 50 sheets, up to 1,000 headers per sheet, arbitrary nesting depth  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. No source code generated during specify/plan phases.
- **Principle II (OOP & SOLID)**: PASSED. Class interfaces follow SRP, OCP, LSP, ISP, DIP.
- **Principle III (GoF Composite Pattern)**: PASSED. Tree nodes implement Composite pattern (`CompositeNode`, `LeafNode`, `WorkspaceForest`).
- **Principle IV (Library-First & TDD)**: PASSED. Path parser service created and tested in core domain library before bridge/UI wiring.
- **Principle V (Self-Contained Excel)**: PASSED. Standard `openpyxl` file processing without COM / MS Excel application dependency.

---

## Project Structure

### Documentation (this feature)

```text
specs/006-excel-hierarchical-import/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Phase 0 architectural decisions & parsing algorithm
├── data-model.md        # Phase 1 domain entities & mapping rules
├── quickstart.md        # Phase 1 verification workflow
├── contracts/
│   └── eel_bridge.json  # Phase 1 Eel RPC API contract
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
├── app/
│   ├── eel_bridge.py          # Eel RPC endpoints returning updated forest roots on import/switch
│   └── main.py                # Desktop application entry point
├── hierarchy_lib/
│   ├── adapters/
│   │   └── excel_adapter.py   # Row 1 header extraction & horizontal path export adapter
│   ├── models/
│   │   ├── base.py            # Component interface
│   │   ├── composite.py       # Composite folder node
│   │   └── leaf.py            # Leaf node
│   └── services/
│       ├── forest.py          # Multi-root tree manager
│       ├── header_service.py  # Header extraction & cleaning service
│       ├── path_generator.py  # Leaf path calculator
│       └── path_parser.py     # NEW: Path-to-Hierarchy parser service
└── web/
    └── js/
        ├── app.js             # Updates workspace canvas when importing file / switching sheet
        ├── drag_drop.js       # Drag & drop handler
        └── tree_renderer.js   # Tree canvas renderer

tests/
├── integration/
│   └── test_eel_bridge.py     # Integration tests for Eel backend endpoints with roots payload
└── unit/
    ├── test_path_parser.py    # NEW: Unit tests for path parsing & tree generation
    ├── test_excel_adapter.py  # Unit tests for Excel adapter
    └── test_header_service.py # Unit tests for header extraction
```

---

## Implementation Sequence

### Phase 1: Core Domain Library (TDD)
1. Create `tests/unit/test_path_parser.py` covering:
   - Nested path parsing (`Root\Folder\Leaf` $\rightarrow$ `Root` -> `Folder` -> `Leaf`)
   - Common ancestor prefix merging (`Root\Folder\A`, `Root\Folder\B`)
   - Single segment headers (`RootField`)
   - Whitespace trimming and delimiter cleanup (` \A\\B\C\ `)
   - Empty/blank header lists
2. Implement `src/hierarchy_lib/services/path_parser.py` (`PathParserService`).

### Phase 2: Excel Adapter & Eel RPC Bridge
1. Update `src/app/eel_bridge.py`:
   - In `import_excel_file`: parse active sheet's headers using `PathParserService`, replace active `forest`, and return `"roots": forest.to_dict()["roots"]`.
   - In `switch_active_sheet`: parse new sheet's headers using `PathParserService`, replace active `forest`, and return `"roots": forest.to_dict()["roots"]`.
2. Update `tests/integration/test_eel_bridge.py` to verify `roots` payload on import and sheet switch.

### Phase 3: Frontend Web UI Integration
1. Update `src/web/js/app.js`:
   - In `handleImportExcelFile`: call `this.updateUI(res.roots)` when response contains `roots`.
   - In `handleSwitchSheet`: call `this.updateUI(res.roots)` when response contains `roots`.
2. Verify end-to-end user experience in browser canvas.

---

## Complexity Tracking

No unusual architectural complexity. Extends existing clean architecture and GoF Composite hierarchy with a dedicated single-responsibility `PathParserService`.
