# Test Data Model & Entities: Full-Project Comprehensive Automated Test Suite

**Feature**: 034-full-project-test-suite  
**Date**: 2026-08-17  

---

## 1. Test Suite Entities & Structure

### E2E Test Suite Matrix (`tests/e2e/`)
| Module Name | Purpose / Domain | Key Selectors / Actions |
|---|---|---|
| `test_tree_crud_and_modals.py` | Root creation, adding child nodes, node renaming, deleting, collapsing/expanding | `#btnCreateRootEmpty`, `#btnAddRootHeader`, `#nodeModal`, `.action-btn.add-child`, `.action-btn.rename-node`, `.action-btn.delete`, `.node-toggle`, `#btnExpandAll`, `#btnCollapseAll` |
| `test_view_modes_and_renderers.py` | Tree, Matrix, Unique Levels, leaf-first grouping, duplicate matching highlight | `#btnViewTree`, `#btnViewMatrix`, `#btnViewUniqueLevels`, `#treeView`, `#excelBlockView`, `#uniqueLevelView`, `.level-header-chip`, `.highlight-match-sync` |
| `test_multi_sheet_and_excel_lifecycle.py` | File import, sheet switching, dirty tracking, unsaved changes modal, template export | `#btnImportExcel`, `#btnRefresh`, `#btnExportExcel`, `#activeSheetSelector`, `#unsavedModal`, `#btnUnsavedCancel`, `#btnUnsavedDiscard`, `#btnUnsavedSave`, `#templateStatusBadge` |
| `test_drag_and_drop.py` | Catalog-to-tree drop, 3 zones (`BEFORE_SIBLING`, `AFTER_SIBLING`, `NEST_CHILD`), cycle prohibition | `.sidebar-header-item`, `.tree-node-content`, `.drop-zone-before`, `.drop-zone-after`, `.drop-zone-inside`, `.toast-warning` |
| `test_settings_and_preferences.py` | Custom delimiter (`\`, `/`, `.`), default data type, settings modal save/reset/cancel | `#btnSettings`, `#settingsModal`, `#inputSettingDelimiter`, `#selectSettingDefaultType`, `#btnSettingsSave`, `#btnSettingsReset`, `#btnSettingsCancel` |
| `test_sidebar_tabs_and_resizer.py` | Tab switching (catalog vs paths), live search, vertical strip, resizer drag/reset, catalog sheet selector | `#sidebarTabSelector`, `#sidebarSearch`, `#btnToggleSidebarCollapse`, `#btnExpandSidebarStrip`, `#sidebarCollapsedStrip`, `#sidebarResizer`, `#catalogSheetSelector` |
| `test_navigation_and_i18n.py` | Bilingual switching (UA/EN), toast notification styles and lifecycle | `#langBtnUk`, `#langBtnEn`, `.toast`, `.toast-info`, `.toast-success`, `.toast-warning`, `.toast-error` |

---

## 2. Standard Test State Invariants

- **Isolation Invariant**: Each test starts with `root_nodes = []`, `sheet_forests = {}`, `current_active_sheet = None`, and `current_template_path = None`.
- **Visibility Invariant**: Every assertion checking for element presence verifies `to_be_visible()`.
- **Zero-Bypass Invariant**: Controls are interacted with exclusively through their user-facing state.
