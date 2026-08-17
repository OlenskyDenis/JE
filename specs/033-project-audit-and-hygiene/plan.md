# Implementation Plan: Project Audit, Hygiene Enforcement & Modular Architecture Refactor

**Branch**: `033-project-audit-and-hygiene` | **Date**: 2026-08-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from [`specs/033-project-audit-and-hygiene/spec.md`](spec.md)

---

## Summary

Conduct a comprehensive project audit, eliminate 13 dead CSS selectors from `src/web/css/style.css`, remove duplicate type mapping loops in backend `eel_bridge.py`, and decompose monolithic source files (`app.js`, `eel_bridge.py`, `unique_level_renderer.js`, `excel_adapter.py`) into modular components strictly obeying Constitution Principle VIII ($\le 200$ lines per source file) and downward-only dependency flow (Principle II).

---

## Technical Context

**Language/Version**: Python 3.10+ & Vanilla JavaScript (ES2022)  
**Primary Dependencies**: Eel (WebSocket JSON-RPC), openpyxl, pytest, playwright  
**Storage**: In-memory `sheet_forests`, atomic `settings.json`, multi-sheet `.xlsx` files  
**Testing**: pytest (100% pass rate, zero warnings, automated AST architecture linters)  
**Target Platform**: Desktop (Windows / Cross-platform Chromium Eel)  
**Project Type**: Desktop GUI / Hybrid Web-Python App  

---

## Constitution & Modularity Check

### 1. Principle VI: System Map & Context Routing Gate
- [x] Loaded `.specify/system_map.md` Master Router Hub.
- [x] Loaded relevant modular map(s) in `.specify/system_map/` (`controllers_and_rpc.md`, `views_and_ui.md`, `infrastructure_and_adapters.md`, `tests_and_quality.md`).

### 2. Principle VIII: 200-Line Modularity Threshold Check

| File to Touch | Current Line Count | Exceeds 200 Lines? | Decomposition / Refactoring Plan |
|---|:---:|:---:|---|
| `src/web/js/app.js` | 1,324 | **Yes** | Decompose into `modal_manager.js` (~170L), `sidebar_controller.js` (~150L), `view_mode_manager.js` (~130L), `app.js` (~160L). |
| `src/web/js/unique_level_renderer.js` | 329 | **Yes** | Split into `unique_level_extractor.js` (~140L) and `unique_level_renderer.js` (~180L). |
| `src/app/eel_bridge.py` | 431 | **Yes** | Split into `session_manager.py` (~150L), `node_controller.py` (~110L), and `eel_bridge.py` (~120L). |
| `src/hierarchy_lib/adapters/excel_adapter.py` | 227 | **Yes** | Split into `excel_reader.py` (~120L), `excel_writer.py` (~110L), and facade `excel_adapter.py` (~35L). |
| `src/web/css/style.css` | 1,664 | Exempt | Prune 13 dead selectors; exempt from 200L rule per Principle VIII. |
| `src/web/js/i18n.js` | 477 | Exempt | Static bilingual dictionary; exempt from 200L rule per Principle VIII. |
| `src/web/index.html` | 288 | Exempt | Declarative layout; exempt from 200L rule per Principle VIII. |

---

## Architecture & Phased Implementation Plan

### Phase 1: Dead CSS Pruning & Backend DRY Session Extraction
1. **Prune Dead CSS**: Remove 13 unused classes from `src/web/css/style.css` (`.badge-sheet`, `.matrix-tier-0..3`, `.radio-card`, `.radio-group`, `.radio-label`, `.sidebar-tab-btn`, `.toast-error..warning`).
2. **Decompose Backend Adapters**:
   - Extract `ExcelReader` into `src/hierarchy_lib/adapters/excel_reader.py` ($\le 200$ lines).
   - Extract `ExcelWriter` into `src/hierarchy_lib/adapters/excel_writer.py` ($\le 200$ lines).
   - Retain `ExcelHierarchyAdapter` in `excel_adapter.py` as a thin delegating facade ($\le 50$ lines).
3. **Decompose Eel Application Layer**:
   - Extract `SessionManager` into `src/app/session_manager.py` with unified DRY header parsing and `_apply_types` logic ($\le 200$ lines).
   - Extract `NodeController` into `src/app/node_controller.py` for node mutations ($\le 200$ lines).
   - Streamline `src/app/eel_bridge.py` as pure `@eel.expose` router ($\le 200$ lines).

### Phase 2: Frontend Monolith Modularization
1. **Decompose Unique Level Renderer**:
   - Create `src/web/js/unique_level_extractor.js` for pure tree traversal and leaf-first partitioning.
   - Streamline `src/web/js/unique_level_renderer.js` for DOM generation and event bindings.
2. **Decompose Application Controller**:
   - Create `src/web/js/modal_manager.js` for add/edit/batch/unsaved/settings modal dialogs.
   - Create `src/web/js/sidebar_controller.js` for tabs, search filter, resizer, and collapse strip.
   - Create `src/web/js/view_mode_manager.js` for view mode coordinator and canvas double-click routing.
   - Streamline `src/web/js/app.js` as master bootstrap and event bus.
3. **Update Declarative Markup**:
   - Update `src/web/index.html` with `<script>` tags in correct dependency order.

### Phase 3: Automated Quality Linters & System Map Parity
1. **Add Modularity Guardrail Test**:
   - In `tests/unit/test_architecture_contracts.py`, implement `test_file_line_count_thresholds()` asserting `line_count <= 200` for all non-exempt `.py` and `.js` files.
2. **Update Frontend Contract Tests**:
   - In `tests/unit/test_frontend_contracts.py`, assert presence and integrity of all newly created scripts.
3. **Synchronize System Maps**:
   - Update `.specify/system_map.md` and `.specify/system_map/*.md` to reflect new components and 84+ test metrics.

---

## Project Structure

```text
specs/033-project-audit-and-hygiene/
├── spec.md              # Feature specification with clarifications & cleanup matrix
├── plan.md              # This technical architecture & phased plan
├── research.md          # Technical research & architectural decisions
├── data-model.md        # Component interfaces, class models & line budgets
├── quickstart.md        # Rapid validation & test run commands
├── checklists/
│   └── requirements.md  # 16/16 Spec Quality Gate Checklist
└── contracts/
    └── eel_bridge.json  # RPC schema & architectural invariants
```

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| *None* | *Architecture fully complies with Constitution Principles I–VIII* | *N/A* |
