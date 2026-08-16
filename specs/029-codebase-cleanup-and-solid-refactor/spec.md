# Feature Specification: Codebase Cleanup and SOLID Refactor

**Feature Branch**: `029-codebase-cleanup-and-solid-refactor`

**Created**: 2026-08-16

**Status**: Draft

**Input**: User description: "029-codebase-cleanup-and-solid-refactor: Complete architectural decoupling (DIP/SOLID), elimination of dead files (base.py, composite.py, leaf.py, path_generator.py), unused RPC endpoints, zombie tests, and system map synchronization"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Architectural Decoupling & Dependency Inversion (Priority: P1) 🎯 MVP

As a developer and system architect, I want core domain models (`HierarchyNode`, `WorkspaceForest`, `PathParserService`, `ExcelHierarchyAdapter`) to be completely decoupled from infrastructure/persistence services (`SettingsService`), so that business logic can be tested and reused in any context without implicit global state or file I/O dependencies.

**Why this priority**: Violating the Dependency Inversion Principle (DIP) tightly couples low-level data structures to file persistence, hindering test isolation and architectural extensibility.

**Independent Test**: Instantiate `HierarchyNode`, `WorkspaceForest`, and `PathParserService` without configuring or mocking `SettingsService`; verify that `get_absolute_path()`, `to_dict()`, and `parse_header_paths()` work reliably with explicit or default delimiters.

**Acceptance Scenarios**:

1. **Given** a `HierarchyNode` instance, **When** `get_absolute_path()` or `to_dict()` is called without specifying a delimiter, **Then** it defaults to standard `"\\"` without reading `SettingsService`.
2. **Given** a `HierarchyNode` instance, **When** `get_absolute_path(delimiter="/")` is called, **Then** it returns the path delimited by `"/"`.
3. **Given** `PathParserService.parse_header_paths()`, **When** invoked without a delimiter, **Then** it defaults to `"\\"` without importing `SettingsService`.
4. **Given** `VALID_DATA_TYPES`, **When** queried or validated by `HierarchyNode` or `SettingsService`, **Then** both reference a single centralized source of truth in `src/hierarchy_lib/models/data_types.py`.
5. **Given** `delete_node(node_id)` in `eel_bridge.py`, **When** invoked for a nested node with a parent, **Then** it directly detaches the node from `node.parent` without redundant or erroneous `isinstance` checks.

---

### User Story 2 - Elimination of Dead Relics & Unused RPC Endpoints (Priority: P2)

As a maintainer, I want all obsolete classes, legacy compatibility wrappers, unused Eel RPC endpoints, and dead frontend methods removed, so that the codebase remains lean, maintainable, and free of confusing phantom APIs.

**Why this priority**: Retaining 19+ unused classes, wrappers, and endpoints increases maintenance overhead and creates ambiguity in system contracts.

**Independent Test**: Verify that the entire desktop UI (tree navigation, modal node editing, inline sheet switching, Excel block matrix view, unique levels view, settings management, and template export) remains 100% functional while all deleted endpoints and files are absent.

**Acceptance Scenarios**:

1. **Given** `src/hierarchy_lib/models/`, **When** inspected, **Then** `base.py`, `composite.py`, and `leaf.py` are completely removed, and all codebase imports point directly to `HierarchyNode`.
2. **Given** `src/hierarchy_lib/services/`, **When** inspected, **Then** `path_generator.py` is completely removed.
3. **Given** `src/app/eel_bridge.py`, **When** inspected, **Then** legacy/unused endpoints (`import_excel`, `export_excel`, `rename_node`, `update_node_type`, `get_sheet_headers`, `get_workspace_tree`, `export_reorganized_row1`) are removed.
4. **Given** `src/hierarchy_lib/adapters/excel_adapter.py`, **When** inspected, **Then** unused methods (`import_from_file`, `export_to_file`, `infer_column_types`, `export_horizontal_row1_leaf_paths`) and the unused `Counter` import are removed.
5. **Given** `src/web/js/`, **When** inspected, **Then** dead methods (`handleExportReorganizedRow1` in `app.js`), redundant globals (`window.I18N_DICTIONARIES`, `getTypeBadgeLabel` in `i18n.js`), and obsolete DOM attributes (`dataset.isContainer` in `tree_renderer.js`) are removed.

---

### User Story 3 - Test Suite Modernization & Zombie Test Deletion (Priority: P2)

As a QA engineer and developer, I want all zombie tests (which test obsolete Feature 001/008 code) deleted and contract tests updated, so that 100% of test assertions validate active production behavior.

**Why this priority**: Zombie tests give a false sense of security and artificially force developers to maintain obsolete functions.

**Independent Test**: Run `python -m pytest`; verify that all tests pass cleanly without errors and without executing tests for retired modules.

**Acceptance Scenarios**:

1. **Given** `tests/unit/`, **When** test suite is run, **Then** `test_excel_export.py`, `test_excel_import.py`, and `test_path_generator.py` are deleted and not executed.
2. **Given** `tests/unit/test_frontend_contracts.py`, **When** executed, **Then** it does not assert the presence of `getTypeBadgeLabel` and strictly asserts active I18n methods (`t`, `getTypeLabel`).
3. **Given** `tests/unit/test_excel_adapter.py`, **When** executed, **Then** tests targeting retired methods (`test_infer_column_types_from_excel_cells`, `test_export_horizontal_row1_leaf_paths`) are removed.
4. **Given** `tests/integration/test_eel_bridge.py`, **When** executed, **Then** all tests target active production RPC endpoints (`import_excel_file`, `save_template_sync`, `update_node`, `delete_node`, `move_node`, `add_node`, `switch_active_sheet`, `refresh_excel_session`).

---

### User Story 4 - System Map & Constitution Retirement Gate Synchronization (Priority: P3)

As a software architect, I want `.specify/system_map.md` and `constitution.md` updated to reflect the streamlined architecture and enforce an explicit "Retirement Verification Gate" in future SDD cycles.

**Why this priority**: Prevents future features from leaving behind deprecated aliases or uncleaned endpoints.

**Independent Test**: Inspect `.specify/system_map.md` to confirm all removed items are marked `🔴 Retired`, and check `constitution.md` for the ratified Retirement Gate workflow rule.

**Acceptance Scenarios**:

1. **Given** `.specify/system_map.md`, **When** reviewed, **Then** component inventories, RPC lists, and architecture diagrams accurately reflect the single `HierarchyNode` model and active RPC endpoints.
2. **Given** `.specify/memory/constitution.md`, **When** reviewed, **Then** Principle VI and Workflow Controls mandate a Retirement Gate checklist during feature task planning.

---

## Edge Cases

- **Zero-Data / Clean-Slate Start**: How does `delete_node` handle deleting the very last root node? System gracefully transitions to empty state (`treeEmptyState` visible) without runtime errors.
- **Missing or Corrupted `settings.json`**: When `SettingsService.load_settings()` encounters a missing or malformed JSON file, it safely falls back to default settings (`"\\"` delimiter and `"Text"` default type) without crashing.
- **Calling `HierarchyNode.get_absolute_path()` on Root Nodes**: Root nodes (where `parent is None`) return `self.name` regardless of the delimiter passed.
- **Dynamic Folder-to-Leaf Transition**: When a parent node loses its last remaining child via `remove_child()`, its `is_folder` property dynamically evaluates to `False`, while preserving its configured `data_type`.
- **Eel RPC Boundary Injection**: The frontend RPC bridge (`eel_bridge.py`) explicitly queries active delimiter from `SettingsService` and passes it to domain serialization (`forest.to_dict(delimiter=...)`), ensuring UI always receives formatted paths according to user settings.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST decouple domain models (`HierarchyNode`, `WorkspaceForest`, `PathParserService`, `ExcelHierarchyAdapter`) from direct `SettingsService` imports, defaulting delimiter parameter to `"\\"` and default data type to `"Text"`.
- **FR-002**: System MUST centralize `VALID_DATA_TYPES` tuple and type validation functions in `src/hierarchy_lib/models/data_types.py`.
- **FR-003**: System MUST update `HierarchyNode` and `SettingsService` to import `VALID_DATA_TYPES` from `src/hierarchy_lib/models/data_types.py`.
- **FR-004**: System MUST simplify `delete_node()` in `eel_bridge.py` to directly call `node.parent.remove_child(node.id)` without `isinstance` checks.
- **FR-005**: System MUST delete `src/hierarchy_lib/models/base.py`, `src/hierarchy_lib/models/composite.py`, and `src/hierarchy_lib/models/leaf.py`, and update all imports across tests/app to `from src.hierarchy_lib.models.node import HierarchyNode`.
- **FR-006**: System MUST delete `src/hierarchy_lib/services/path_generator.py`.
- **FR-007**: System MUST delete obsolete RPC endpoints in `src/app/eel_bridge.py`: `import_excel`, `export_excel`, `rename_node`, `update_node_type`, `get_sheet_headers`, `get_workspace_tree`, and `export_reorganized_row1`.
- **FR-008**: System MUST delete obsolete methods in `src/hierarchy_lib/adapters/excel_adapter.py`: `import_from_file`, `export_to_file`, `infer_column_types`, and `export_horizontal_row1_leaf_paths`, and remove unused `Counter` import.
- **FR-009**: System MUST delete `handleExportReorganizedRow1` from `src/web/js/app.js`.
- **FR-010**: System MUST delete `getTypeBadgeLabel` and `window.I18N_DICTIONARIES` export from `src/web/js/i18n.js`.
- **FR-011**: System MUST remove `wrapper.dataset.isContainer = isFolder;` from `src/web/js/tree_renderer.js`.
- **FR-012**: System MUST delete zombie test files `tests/unit/test_excel_export.py`, `tests/unit/test_excel_import.py`, and `tests/unit/test_path_generator.py`.
- **FR-013**: System MUST update `tests/unit/test_frontend_contracts.py` to remove `getTypeBadgeLabel` assertion.
- **FR-014**: System MUST update `.specify/system_map.md` to reflect the retired components, updated RPC list, and streamlined models.
- **FR-015**: System MUST update `.specify/memory/constitution.md` to document the Retirement Verification Gate.

---

### Key Entities

- **HierarchyNode**: Single dynamic node representing both folders and leaves depending on `len(children) > 0`. Independent of persistence.
- **WorkspaceForest**: In-memory container of tree roots for the active sheet, providing multi-root path collection and serialization.
- **DataTypes (`data_types.py`)**: Centralized repository of standard Excel column data types (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`) and validation logic.
- **SettingsService**: Infrastructure service managing `settings.json` file persistence, atomic saves, and configuration retrieval.
- **EelBridge**: Application orchestration layer bridging Eel RPC calls to domain operations and injecting active settings into domain calls.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of unit and integration tests pass with `python -m pytest` with zero failures.
- **SC-002**: Zero direct imports of `SettingsService` within `src/hierarchy_lib/models/` and `src/hierarchy_lib/services/path_parser.py`.
- **SC-003**: Codebase size reduced by removing 4 dead source files (`base.py`, `composite.py`, `leaf.py`, `path_generator.py`) and 3 dead test files.
- **SC-004**: 7 dead RPC endpoints removed from `eel_bridge.py` without breaking any frontend functionality.
- **SC-005**: 100% synchronization between `.specify/system_map.md` and active codebase components.

---

## Assumptions

- Python 3.10+ runtime with `openpyxl`, `eel`, and standard library modules (`tkinter`, `json`, `os`, `uuid`).
- Backward compatibility with Feature 001 Column A import/export is officially terminated in favor of the multi-sheet Row 1 horizontal template pipeline (Feature 014/016/020).
- Frontend JavaScript runs in Chromium/Eel environment and interacts with backend purely via active Eel exposed functions (`import_excel_file`, `save_template_sync`, `switch_active_sheet`, `refresh_excel_session`, `add_node`, `update_node`, `delete_node`, `move_node`, `get_settings`, `update_settings`, `reset_settings`, `open_file_dialog`, `save_file_dialog`).
