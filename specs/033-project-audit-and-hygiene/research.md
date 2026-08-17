# Technical Research: Project Audit, Hygiene & Modularity Refactor

**Feature Branch**: `033-project-audit-and-hygiene`  
**Date**: 2026-08-17  
**Spec**: [spec.md](spec.md)

---

## 1. Research Objectives & Scope

This research evaluates the technical strategies for:
1. Pruning 13 dead CSS selectors from `src/web/css/style.css`.
2. Extracting duplicate header parsing and type mapping logic in Python backend (`eel_bridge.py`).
3. Decomposing monolithic files (`app.js` [1324 lines], `eel_bridge.py` [431 lines], `unique_level_renderer.js` [329 lines], `excel_adapter.py` [227 lines]) to strictly satisfy Constitution Principle VIII ($\le 200$ lines per source file).
4. Enforcing automated line-count limits in `test_architecture_contracts.py`.

---

## 2. Research Decisions & Analysis

### Decision 1: Frontend Decomposition Architecture (Vanilla JS Namespace Delegation)

* **Decision**: Decompose `app.js` into 4 focused modules:
  - `src/web/js/modal_manager.js`: Encapsulates all modal lifecycle (Add Node, Edit/Rename Node, Batch Edit Notice, Unsaved Changes Prompt, Settings Modal).
  - `src/web/js/sidebar_controller.js`: Encapsulates sidebar tabs, search input filtering, resizer drag-to-resize, and collapsed strip toggle.
  - `src/web/js/view_mode_manager.js`: Coordinates active view mode switching (Tree, Excel Block, Unique Level) and dispatches canvas rendering.
  - `src/web/js/app.js`: Master application bootstrap, event listener registration, and Eel RPC dispatch coordinator.
* **Rationale**: Adheres to the user's clarified direction (Option A: Facade delegation via `window` namespace). Eliminates the need for Node.js build tools (Webpack, Rollup, Vite) or `<script type="module">` CORS complexities in local Eel webviews, keeping the desktop runtime ultra-fast, zero-dependency, and easy to inspect.
* **Alternatives Considered**:
  - *ES6 Modules (`<script type="module">`)*: Rejected because local file loading in older WebViews or standalone Eel offline contexts can run into strict CORS origins if file protocol is used, and requires altering script loading semantics.
  - *Monolithic Class preservation*: Rejected because 1,324 lines directly violates Constitution Principle VIII (200-line standard).

---

### Decision 2: Unique Level Renderer Decomposition

* **Decision**: Split `src/web/js/unique_level_renderer.js` (329 lines) into:
  - `src/web/js/unique_level_extractor.js` (~140 lines): Pure algorithmic module (`UniqueLevelExtractor`) that traverses composite trees, extracts levels, groups duplicate names, and partitions nodes into leaf-first and branch subgroups.
  - `src/web/js/unique_level_renderer.js` (~180 lines): DOM generation module (`UniqueLevelRenderer`) that builds cards, badges, counts, and binds inline double-click editing events.
* **Rationale**: Separates pure data transformation (business logic) from DOM presentation (UI rendering), adhering directly to SRP (SOLID Principle 1) and KISS.
* **Alternatives Considered**:
  - *Shrinking code by minification/dense one-liners*: Rejected by `CodeStyle.md` and `KISS.md` (readability over cleverness).

---

### Decision 3: Backend Eel RPC & Session Manager Decomposition

* **Decision**: Decompose `src/app/eel_bridge.py` (431 lines) into:
  - `src/app/session_manager.py` (~150 lines): Houses `sheet_forests`, `current_file_path`, `current_active_sheet`, `current_template_path`, and unified DRY Excel session synchronization (`import_file`, `refresh_session`, `switch_sheet`, `save_template`).
  - `src/app/node_controller.py` (~110 lines): Houses pure node mutation operations (`add_node`, `update_node`, `delete_node`, `move_node`) and zone insertion routing.
  - `src/app/eel_bridge.py` (~120 lines): Clean `@eel.expose` router forwarding calls to `session_manager`, `node_controller`, `SettingsService`, and `FileDialogService`.
* **Rationale**: Solves the 431-line violation, eliminates triple duplication of `_apply_types` loops across `import`/`refresh`/`switch`, and enforces SRP.
* **Alternatives Considered**:
  - *Moving RPCs directly into `hierarchy_lib/`*: Strictly rejected by Constitution Principle II & downward-only dependency flow (`hierarchy_lib` must never know about Eel or RPC envelopes).

---

### Decision 4: Excel Adapter Decomposition with Public Facade

* **Decision**: Decompose `src/hierarchy_lib/adapters/excel_adapter.py` (227 lines) into:
  - `src/hierarchy_lib/adapters/excel_reader.py` (~120 lines): `ExcelReader` handling `openpyxl` streaming read (Row 1 headers, number formats, sheet names).
  - `src/hierarchy_lib/adapters/excel_writer.py` (~110 lines): `ExcelWriter` handling fresh `openpyxl.Workbook` construction, horizontal leaf path writing, and format mapping.
  - `src/hierarchy_lib/adapters/excel_adapter.py` (~35 lines): `ExcelHierarchyAdapter` public facade delegating to reader and writer.
* **Rationale**: Maintains 100% backward compatibility for all existing unit tests and fixtures while bringing each file safely below 200 lines.
* **Alternatives Considered**:
  - *Deleting `ExcelHierarchyAdapter` class name*: Rejected because it would require rewriting numerous test imports without architectural benefit.

---

### Decision 5: Automated Modularity Threshold Architecture Linter

* **Decision**: Add `test_file_line_count_thresholds()` in `tests/unit/test_architecture_contracts.py`.
* **Rules**:
  - Iterates over all `.py` files in `src/` and `.js` files in `src/web/js/`.
  - Asserts `line_count <= 200`.
  - Exempts documented files: `src/web/js/i18n.js` (translation dictionaries), `src/web/css/style.css` (central stylesheet), and `src/web/index.html` (declarative layout).
* **Rationale**: Automates Constitution Principle VIII verification so regressions are caught in pre-commit hooks and CI immediately.
