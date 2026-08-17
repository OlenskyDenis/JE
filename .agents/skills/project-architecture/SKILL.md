---
name: project-architecture
description: >
  Architectural map and dependency guide for the JE (Database Hierarchy Creator) project.
  Use when navigating the codebase, deciding where to place new code, or understanding layer boundaries.
---

# JE Project Architecture Guide

> **Purpose:** Quick-reference map for navigating the JE codebase without repeated `list_dir`/`view_file` exploration.

## Stack Overview

| Layer | Technology | Location |
|---|---|---|
| Backend | Python 3.10+, Eel (gevent) | `src/app/`, `src/hierarchy_lib/` |
| Frontend | Vanilla JS, HTML5, CSS3 | `src/web/` |
| Bridge | Eel RPC (@eel.expose) | `src/app/eel_bridge.py` |
| Data | openpyxl (Excel .xlsx) | `src/hierarchy_lib/adapters/` |
| Tests | pytest, Playwright | `tests/unit/`, `tests/integration/`, `tests/e2e/` |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (src/web/)                   │
│                                                         │
│  index.html ← css/style.css, css/drag_drop.css          │
│                                                         │
│  js/app.js ────────────── Entry point, App singleton     │
│  js/tree_renderer.js ──── Tree view rendering            │
│  js/excel_block_renderer.js ── Matrix/block view         │
│  js/unique_level_renderer.js ── Unique levels view       │
│  js/drag_drop.js ──────── DragDropHandler singleton      │
│  js/i18n.js ───────────── I18n singleton (UK/EN)         │
│                                                         │
│  eel.add_node() ──┐                                     │
│  eel.move_node() ─┤ Async RPC calls                     │
│  eel.delete_node()┤                                     │
│  etc.            ─┘                                     │
└──────────┬──────────────────────────────────────────────┘
           │ Eel WebSocket (JSON serialization)
┌──────────▼──────────────────────────────────────────────┐
│             EEL BRIDGE (src/app/eel_bridge.py)           │
│                                                         │
│  @eel.expose functions → Dict[str, Any]                  │
│  Global state: forest, sheet_forests, current_file_path  │
│  All methods: try/except → {"success": bool, ...}       │
│                                                         │
│  Orchestrates: models + services + adapters              │
└──────────┬──────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│         HIERARCHY LIB (src/hierarchy_lib/)               │
│                                                         │
│  models/                                                │
│    node.py ──── HierarchyNode (Composite pattern)       │
│    data_types.py ── VALID_DATA_TYPES, validate_data_type│
│                                                         │
│  services/                                              │
│    forest.py ──────── WorkspaceForest (multi-root tree) │
│    path_parser.py ─── PathParserService (header→tree)   │
│    header_service.py ─ HeaderService                    │
│    settings_service.py SettingsService (delimiter, etc.) │
│    dialog_service.py ─ FileDialogService (OS dialogs)   │
│                                                         │
│  adapters/                                              │
│    excel_adapter.py ── ExcelHierarchyAdapter (openpyxl) │
└─────────────────────────────────────────────────────────┘
```

## Layer Dependency Rules

```
Frontend (JS)  →  Eel Bridge  →  Services  →  Models
                                     ↓
                                  Adapters (Excel)
```

* **Models** have ZERO external dependencies (only `uuid`, `typing`). Models never import services or adapters.
* **Services** depend on Models. Services never import from `src/app`.
* **Adapters** depend on Models + external libs (openpyxl). Adapters never import services.
* **Eel Bridge** orchestrates Services + Adapters. It is the ONLY module importing from both.
* **Frontend JS** calls bridge via `eel.<function>()`. Never bypasses bridge.

## Key Domain Concepts

| Concept | Implementation | Description |
|---|---|---|
| **HierarchyNode** | `models/node.py` | Unified Composite: folder if `children > 0`, leaf if `children == 0`. Dynamic role — no separate classes. |
| **WorkspaceForest** | `services/forest.py` | Multi-root tree container. Manages add/remove/move/find across all root trees. |
| **Eel Bridge** | `app/eel_bridge.py` | Stateful RPC layer with global `forest` and `sheet_forests` dict. Each exposed function = one UI action. |
| **Delimiter** | `settings_service.py` | Configurable path separator (default `\`). Used in path generation and parsing. |
| **Sheet Session** | `eel_bridge.py` globals | `sheet_forests: Dict[str, WorkspaceForest]` — one forest per Excel sheet, persisted in-memory during session. |

## Spec Workflow

Features are documented in `specs/NNN-feature-name/` with standardized structure:
- `spec.md` — Feature specification
- `plan.md` — Implementation plan
- `tasks.md` — Task breakdown (checklist)
- `research.md` — Background research (optional)
- `data-model.md` — Data model changes (optional)

## Where to Put New Code

| I need to... | Put it in... |
|---|---|
| Add a new Eel-exposed function | `src/app/eel_bridge.py` + corresponding JS call in `src/web/js/app.js` |
| Add domain logic | `src/hierarchy_lib/services/` (new or existing service) |
| Add a new data model | `src/hierarchy_lib/models/` |
| Add external integration | `src/hierarchy_lib/adapters/` |
| Add a new UI view/renderer | `src/web/js/new_renderer.js` + register in `index.html` |
| Add styles | `src/web/css/style.css` (or new CSS file if concern is distinct) |
| Add i18n keys | `src/web/js/i18n.js` — both `uk` and `en` translation objects |
| Add unit tests | `tests/unit/` |
| Add integration tests | `tests/integration/` |
| Add E2E tests | `tests/e2e/` |
| Document a feature | `specs/NNN-feature-name/` |
