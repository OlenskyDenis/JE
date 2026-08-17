# JE Project Knowledge Base & Engineering Memo

> **Authoritative Technical Reference** for architectural invariants, domain rules, Eel bridge contracts, Excel streaming details, and testing recipes in **JE (Database Hierarchy Creator)**.

---

## 1. Architectural Boundaries & Layering (SOLID & Modular KISS)

The system is strictly divided into 3 isolated layers with modular components satisfying the **Constitution Principle VIII $\le 200$ lines** invariant:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Modular Frontend Layer (src/web/js/)                                 │
│    - app.js (Orchestrator & Event Bus)                                  │
│    - modal_manager.js, sidebar_controller.js, view_mode_manager.js      │
│    - session_controller.js, settings_controller.js                     │
│    - tree_renderer.js, excel_block_renderer.js, drag_drop.js            │
│    - unique_level_renderer.js, unique_level_extractor.js, i18n.js       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ JSON RPC Calls
┌────────────────────────────────────▼────────────────────────────────────┐
│ 2. Desktop Application Layer (src/app/)                                 │
│    - eel_bridge.py (@eel.expose Router & IPC Dispatcher)                │
│    - session_manager.py (Session Forest State & Template Sync)          │
│    - node_controller.py (Node CRUD Operations & Zone Mutations)         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Pure Python Invocations
┌────────────────────────────────────▼────────────────────────────────────┐
│ 3. Core Domain Layer (src/hierarchy_lib/)                               │
│    - models/ (HierarchyNode, data_types.py)                             │
│    - services/ (WorkspaceForest, PathParserService, SettingsService)    │
│    - adapters/ (ExcelHierarchyAdapter facade -> ExcelReader & Writer)   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Layer Rules:
1. **`hierarchy_lib` must NEVER import `eel`, `src.app`, or UI elements.** It must remain 100% testable in headless Python environments without any GUI or web server running.
2. **`src/app/eel_bridge.py` is the routing gateway for all frontend RPC calls.** It delegates to `SessionManager`, `NodeController`, `SettingsService`, and `FileDialogService`.
3. **`src/web/` communicates with Python ONLY via `eel.<exposed_function>(...)`.** All user-facing strings must use `I18n.t("key")` from `i18n.js` with full Ukrainian (`uk`) and English (`en`) parity.
4. **Principle VIII Guardrail:** All non-exempt source files must have $\le 200$ lines (enforced automatically in `test_file_line_count_thresholds()`).

---

## 2. Eel Desktop Bridge & RPC Contracts

### Standard Return Envelope
Every exposed Eel RPC endpoint must return a structured dictionary:
* **Success:** `{"success": True, "data": ...}` or `{"success": True, "roots": [...]}`
* **Error:** `{"success": False, "error": "Error description or i18n translation key"}`

### Eel WebSocket & Lifecycle Quirks:
* **Auto-shutdown Detection:** Eel terminates the Python process when all browser windows disconnect. In automated test environments (e.g. Playwright in `tests/e2e/conftest.py`), auto-shutdown must be suppressed using:
  ```python
  import eel
  eel._detect_shutdown = lambda *args, **kwargs: None
  ```
* **Thread Safety:** Eel runs on Bottle/gevent. Heavy disk operations or file dialogs should not block the event loop indefinitely.

---

## 3. Excel Processing & Multi-Sheet Domain Invariants

### Row 1 Streaming & Ghost Columns:
* **Header Extraction:** `ExcelReader.read_row1_headers_and_types` loads workbooks in `read_only=True` mode, inspecting strictly `max_row=1`.
* **Consecutive Empty Cutoff:** Excel files often report `max_column = 16384` due to blank cell styling. The reader stops scanning once `max_empty_consecutive` (default: 10) consecutive empty cells are met.
* **Column Order Preservation:** Headers must never be sorted alphabetically. Original Excel column sequence ($A \to B \to C \dots$) is strictly preserved.

### Data Types System:
The application supports **9 standard data types**:
1. `Text` (`@`)
2. `Integer` (`0`)
3. `Decimal` (`0.00`)
4. `Currency` (`"$"#,##0.00` / `грн` / `€`)
5. `Percentage` (`0.00%`)
6. `Date` (`yyyy-mm-dd`)
7. `Time` (`hh:mm:ss`)
8. `DateTime` (`yyyy-mm-dd hh:mm:ss`)
9. `Boolean` (`General`)

* Only **leaf nodes** carry active data types. When a node gains children (upgraded to a folder container), its data type is ignored; when its children are deleted (downgraded to a leaf), it reverts to its configured type or fallback (`Text`).

### Multi-Sheet Session Management:
* Each sheet has an independent hierarchy tree stored in `SessionManager.sheet_forests`.
* Re-exporting via `ExcelWriter.export_multi_sheet_template`:
  1. Creates a clean `openpyxl.Workbook()`.
  2. For configured sheets: writes leaf paths and number formats horizontally across Row 1 ($A1, B1, C1\dots$).
  3. For unconfigured sheets: copies original Row 1 headers.
  4. Guarantees zero data rows ($Row \ge 2$) in the exported template file.

---

## 4. Test Fixtures & Deterministic Datasets

All sample test workbooks are maintained under `tests/fixtures/excel_samples/` and can be regenerated at any time using:
```bash
python tests/fixtures/generate_fixtures.py
```

| Fixture File | Focus Area |
| :--- | :--- |
| `standard_hierarchy.xlsx` | 3-level tree (Category $\to$ Subcategory $\to$ Product) with data types. |
| `deep_hierarchy_ragged.xlsx` | 5-6 levels with uneven branch depths and sparse headers. |
| `multisheet_retail.xlsx` | 3 sheets (`Store_East`, `Store_West`, `Warehouse_Central`) with isolated schemas. |
| `cyrillic_and_symbols.xlsx` | Ukrainian Cyrillic, quotes (`« »`, `' "`), slashes, numbers, `#`, `№`. |
| `data_types_matrix.xlsx` | Explicit formatting matrix across all 9 data types. |

---

## 5. UI & E2E Testing Lessons Learned (Engineering Invariants)

> **Golden Rule:** *"Assert what the user sees, not what the DOM contains."*

1. **Visual Visibility Over DOM Presence:**
   - Never rely solely on `expect(locator).to_have_count(N)`. Elements inside containers styled with `display: none` (`.hidden`) exist in the DOM tree but are invisible to users.
   - Always assert visual visibility: `expect(locator.first).to_be_visible()` and `expect(container).not_to_have_class("hidden")`.
2. **Zero Test Bypasses (No Synthetic State Mutating):**
   - Tests must never manually enable disabled inputs or toggle CSS classes (e.g. `el.disabled = false`).
   - If a control should be enabled, the production flow (e.g., `updateSheetSelectors()`) must enable it automatically.
3. **Sub-Controller State Class Contract:**
   - When decomposing JavaScript modules, verify that state synchronization classes (`.hidden`, `.active`, `.sidebar-collapsed`) are explicitly handled during both empty and populated states.

