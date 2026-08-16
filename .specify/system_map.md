# Global System Map: Master Router & Architecture Hub

**Location**: `.specify/system_map.md` (and `.specify/system_map/router.md`)  
**Last Updated**: 2026-08-16  
**Architecture Style**: Modular MVC & Clean Architecture (C4 Model Level 1–2)  
**Governing Principle**: Constitution Principle VI (Modular System Map & Context Routing)

---

## 1. High-Level System Architecture (C4 Context & Container Diagram)

The application is an environment-independent Desktop GUI for modeling, restructuring, and persisting database hierarchies from and into Microsoft Excel (`.xlsx`) files.

```mermaid
graph TD
    subgraph ViewLayer["1. Views & UI (Presentation)"]
        HTML["index.html (Layout & Modals)"]
        TreeRenderer["tree_renderer.js (Tree Canvas)"]
        MatrixRenderer["excel_block_renderer.js (Matrix View)"]
        LevelRenderer["unique_level_renderer.js (Unique Levels)"]
        DragDrop["drag_drop.js (3-Zone D&D)"]
        I18n["i18n.js (Localization Engine)"]
    end

    subgraph ControllerLayer["2. Controllers & RPC Bridge"]
        AppController["app.js (Main App Controller)"]
        EelBridge["eel_bridge.py (JSON-RPC Dispatcher)"]
    end

    subgraph DomainLayer["3. Domain & Models (Pure Logic)"]
        HierarchyNode["HierarchyNode (Dynamic Composite)"]
        DataTypes["data_types.py (9 Excel Types & Validation)"]
        Forest["WorkspaceForest (Multi-Root Canvas)"]
        PathParser["PathParserService (Delimiter Parser)"]
    end

    subgraph InfraLayer["4. Infrastructure & Adapters"]
        ExcelAdapter["ExcelHierarchyAdapter (openpyxl Streaming)"]
        SettingsService["SettingsService (settings.json Persistence)"]
        HeaderService["HeaderService (Trimming & FIFO Dedup)"]
        DialogService["FileDialogService (Native OS Dialogs)"]
    end

    %% Interactions
    HTML <-->|User Events & DOM Binding| AppController
    TreeRenderer & MatrixRenderer & LevelRenderer & DragDrop <--> AppController
    AppController <-->|JSON-RPC via WebSocket| EelBridge
    EelBridge -->|Mutates / Queries| Forest
    EelBridge -->|Injects Config & Parses| PathParser
    EelBridge -->|Invokes IO| ExcelAdapter
    EelBridge -->|Persists / Loads| SettingsService
    EelBridge -->|Spawns Dialogs| DialogService
    Forest --> HierarchyNode
    HierarchyNode --> DataTypes
    ExcelAdapter --> HeaderService
```

---

## 2. Modular System Map Router (MVC Layer Breakdown)

To avoid bloated monolithic context files, the system map is modularized following the **MVC / Clean Architecture** paradigm. Click any link below to explore that layer:

| Architectural Layer | Modular Map File | Description & Contents | Primary Technologies |
|---|---|---|---|
| **1. Model / Domain** | [`.specify/system_map/domain_and_models.md`](system_map/domain_and_models.md) | Pure business logic, `HierarchyNode` dynamic composite, `data_types.py`, `WorkspaceForest`, `PathParserService`, cycle checks, DIP rules. | Python 3.10+ (Standard Library) |
| **2. View / Presentation** | [`.specify/system_map/views_and_ui.md`](system_map/views_and_ui.md) | `index.html` layout, Tree/Matrix/Unique Level renderers, `drag_drop.js`, `i18n.js` dictionaries, and `style.css` dark theme. | Vanilla HTML5, Vanilla JS (ES2022), CSS3 |
| **3. Controller & RPC** | [`.specify/system_map/controllers_and_rpc.md`](system_map/controllers_and_rpc.md) | `app.js` frontend controller, `@eel.expose` RPC endpoints in `eel_bridge.py`, event dispatchers, and application services. | Python Eel, WebSocket JSON-RPC |
| **4. DTOs & Contracts** | [`.specify/system_map/dtos_and_contracts.md`](system_map/dtos_and_contracts.md) | Canonical JSON payload definitions (`HierarchyNodeDTO`, `SettingsDTO`, `ExcelSessionDTO`, `RejectionDTO`). | JSON Schema / DTOs |
| **5. Infrastructure & IO** | [`.specify/system_map/infrastructure_and_adapters.md`](system_map/infrastructure_and_adapters.md) | `ExcelHierarchyAdapter` (openpyxl streaming, Row 1 inspection, multi-sheet export), native OS dialogs, atomic `settings.json`. | openpyxl, Tkinter file dialogs |
| **6. State & Lifecycle** | [`.specify/system_map/state_and_lifecycle.md`](system_map/state_and_lifecycle.md) | Backend multi-sheet session containers (`sheet_forests`, `current_file_path`) and frontend state (`isDirty`, `collapsedNodeIds`). | In-Memory & `localStorage` |
| **7. Quality & Testing** | [`.specify/system_map/tests_and_quality.md`](system_map/tests_and_quality.md) | Complete 76-test suite registry, automated AST architecture linters, and frontend contract verification. | pytest, ast, Python unittest |

---

## 3. Context-Aware Loading Guide for AI & Developers

When working on a specific task or feature, **DO NOT load all source files**. Follow this targeted context routing guide:

* 🎨 **Frontend UI / CSS / View Mode feature**: Load [`.specify/system_map/views_and_ui.md`](system_map/views_and_ui.md) + [`.specify/system_map/dtos_and_contracts.md`](system_map/dtos_and_contracts.md).
* ⚙️ **Backend logic / Excel parsing / Data types**: Load [`.specify/system_map/domain_and_models.md`](system_map/domain_and_models.md) + [`.specify/system_map/infrastructure_and_adapters.md`](system_map/infrastructure_and_adapters.md).
* 🌉 **New RPC endpoint / Settings / Bridge change**: Load [`.specify/system_map/controllers_and_rpc.md`](system_map/controllers_and_rpc.md) + [`.specify/system_map/dtos_and_contracts.md`](system_map/dtos_and_contracts.md).
* 🧠 **Multi-sheet session / Dirty state bug**: Load [`.specify/system_map/state_and_lifecycle.md`](system_map/state_and_lifecycle.md).
* 🧪 **Writing tests / Verifying boundaries**: Load [`.specify/system_map/tests_and_quality.md`](system_map/tests_and_quality.md).

---

## 4. Active System Health & Status Matrix

| Component / Layer | Status | Key Health Guarantee |
|---|:---:|---|
| **Dynamic Composite (`HierarchyNode`)** | 🟢 Active | Unifies folder/leaf dynamically; zero base class bloat. |
| **Data Types Module (`data_types.py`)** | 🟢 Active | Centralized 9 Excel types with case-insensitive validation (OCP). |
| **Multi-Root Forest (`WorkspaceForest`)** | 🟢 Active | Supports 3-zone insertion, cycle prevention, and leaf path resolution. |
| **Path Parser (`PathParserService`)** | 🟢 Active | Supports custom delimiters (`\`, `/`, `::`) with prefix branch merging. |
| **Excel Adapter (`ExcelHierarchyAdapter`)** | 🟢 Active | Read-only streaming, Row 1 only, 0 data rows read, multi-sheet export. |
| **Eel RPC Bridge (`eel_bridge.py`)** | 🟢 Active | 13 clean active endpoints; zero legacy Feature 001 dead RPCs. |
| **Frontend UI (`src/web/`)** | 🟢 Active | 3 view modes (Tree, Matrix, Unique Levels), 2 languages (UK, EN), dark theme. |
| **Test Suite (`pytest`)** | 🟢 Active | 76 tests passing in ~1.1s, 0 warnings, automated AST architecture linters. |
| **Legacy Models / Tests (`base.py`, etc.)** | 🔴 Retired | Completely deleted (Feature 029); enforced by linter. |

---

## 5. Maintenance & Retirement Guidelines

Whenever a new feature is specified (`/speckit.specify`) or planned (`/speckit.plan`):
1. **Load this Router**: Identify which modular map files are affected by the proposed changes.
2. **Consult & Update the Affected Modular Maps**: Ensure any new classes, endpoints, or DOM elements are documented in the corresponding layer map.
3. **Enforce Strict Sunset (Principle II)**: If an entity is replaced, delete it immediately and record it as `🔴 Retired` in the appropriate layer map.
4. **Level-3 Decomposition Guardrail (Principle VI)**: Modular maps in `.specify/system_map/` are kept at Level 2. If any layer map exceeds **15–20 KB (~4 000 tokens)**, decompose it into a Level-3 sub-router and dedicated micro-maps. Sub-routing below this threshold is prohibited to prevent navigational tool hop overhead.
