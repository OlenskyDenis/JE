# Tests & Quality Layer: Verification Registry & Architecture Linters

**Path**: `.specify/system_map/tests_and_quality.md`  
**Architectural Layer**: Quality & Verification  
**Governing Principles**: Constitution Principle IV (TDD & Zero Zombie Tests) & Principle VIII (200-Line Limit)

---

## 1. Test Suite Registry (`tests/`)

The active test suite comprises **86 automated tests** with 100% pass rate and zero third-party warnings.

| Test File | Target Layer | Scope & Responsibilities |
|---|---|---|
| [`tests/unit/test_architecture_contracts.py`](file:///E:/JE/tests/unit/test_architecture_contracts.py) | **Architecture Linter** | AST-level verification: DIP enforcement, YAGNI retired file absence, RPC hygiene, modular system map integrity, and **Constitution Principle VIII $\le 200$ line-count threshold enforcement** across Python and JS sources. |
| [`tests/unit/test_frontend_contracts.py`](file:///E:/JE/tests/unit/test_frontend_contracts.py) | **Frontend Contract** | Verifies all `<script>` tags in `index.html` exist on disk, DOM IDs called in JS exist in HTML, I18n methods exist, bilingual translation key parity (`uk` == `en`), and modular sub-controller exports to `window`. |
| [`tests/integration/test_eel_bridge.py`](file:///E:/JE/tests/integration/test_eel_bridge.py) | **RPC Bridge Integration** | End-to-end user journeys: multi-sheet Excel file import, active sheet switching, drag-and-drop 3-zone additions, cycle prevention rejections, node renames, data type edits, and synchronized multi-sheet template export. |
| [`tests/unit/test_data_types.py`](file:///E:/JE/tests/unit/test_data_types.py) | **Domain / OCP** | Validates the 9 canonical Excel data types, case-insensitive normalization, default fallbacks, and error handling. |
| [`tests/unit/test_composite.py`](file:///E:/JE/tests/unit/test_composite.py) | **Domain / Models** | Dynamic folder/leaf state transitions (`is_folder`), cycle prevention, parent-child detachment, absolute path computation, and DTO serialization. |
| [`tests/unit/test_forest_zone_addition.py`](file:///E:/JE/tests/unit/test_forest_zone_addition.py) | **Domain / Forest** | 3-zone positional node insertion (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`) on root trees and nested branches. |
| [`tests/unit/test_path_parser.py`](file:///E:/JE/tests/unit/test_path_parser.py) | **Domain / Parser** | Parsing sequences of path strings with standard (`\`) and custom (`/`, `::`) delimiters, common prefix folder merging, and column sequence preservation. |
| [`tests/unit/test_excel_adapter.py`](file:///E:/JE/tests/unit/test_excel_adapter.py) | **Infrastructure / IO** | openpyxl read-only streaming, Row 1 scanning with 10-consecutive-empty cutoff, cell number format inspection, and multi-sheet template export with zero data rows. |
| [`tests/unit/test_excel_fixtures.py`](file:///E:/JE/tests/unit/test_excel_fixtures.py) | **Infrastructure / Fixtures** | Validates creation and structure of test Excel workbooks with multiple sheets and format varieties. |
| [`tests/unit/test_settings_service.py`](file:///E:/JE/tests/unit/test_settings_service.py) | **Application / Config** | `settings.json` atomic saving/loading, delimiter validation (1–3 chars), data type validation, and fallback defaults. |
| [`tests/unit/test_header_service.py`](file:///E:/JE/tests/unit/test_header_service.py) | **Application / Service** | Header trimming, deduplication, filtering, and sequence preservation. |
| [`tests/unit/test_dialog_service.py`](file:///E:/JE/tests/unit/test_dialog_service.py) | **Infrastructure / OS** | OS file dialog mocking, cancel handling, and hidden Tkinter root window lifecycle. |

---

## 2. Architecture Governance & Linter Contracts

The file [`tests/unit/test_architecture_contracts.py`](file:///E:/JE/tests/unit/test_architecture_contracts.py) acts as a runtime gate running on every `pytest` execution:
1. **DIP Gate**: Inspects AST of `models/*.py` and raises error if any file imports from `services`, `adapters`, or `app`.
2. **YAGNI Gate**: Asserts that `base.py`, `composite.py`, `leaf.py`, `path_generator.py`, `test_excel_export.py`, `test_excel_import.py`, `test_path_generator.py` are absent.
3. **RPC Boundary Gate**: Asserts that deleted Feature 001 RPCs are not present in `eel_bridge.py`.
4. **Principle VIII Gate**: Enforces that all non-exempt Python source files in `src/` and JavaScript files in `src/web/js/` do not exceed 200 lines.
