# Quickstart & Verification Guide: Full-Project Comprehensive Automated Test Suite

**Feature**: 034-full-project-test-suite  
**Date**: 2026-08-17  

---

## 1. Quick Quality Check (Backend Unit + Integration)

Runs fast syntax, linter, backend unit tests, and integration tests in $< 3$ seconds:
```powershell
python scripts/check_all.py --quick
```

---

## 2. Full Regression Suite (Unit + Integration + E2E Playwright)

Runs the complete 110+ test verification matrix in headless Chromium:
```powershell
python scripts/check_all.py --full
```

---

## 3. Targeted Playwright E2E Suite by Functional Domain

Run specific domain test modules:
```powershell
# 1. Tree CRUD, Modals & Branch Collapsing
python -m pytest tests/e2e/test_tree_crud_and_modals.py -v

# 2. View Modes (Tree, Matrix, Unique Levels with Grouping & Highlights)
python -m pytest tests/e2e/test_view_modes_and_renderers.py -v

# 3. Multi-Sheet Session Lifecycle & Template Export
python -m pytest tests/e2e/test_multi_sheet_and_excel_lifecycle.py -v

# 4. Drag and Drop, 3 Zones & Cycle Detection
python -m pytest tests/e2e/test_drag_and_drop.py -v

# 5. Settings, Delimiters & Default Data Types
python -m pytest tests/e2e/test_settings_and_preferences.py -v

# 6. Sidebar Tabs, Search, Collapse Strip & Resizer
python -m pytest tests/e2e/test_sidebar_tabs_and_resizer.py -v

# 7. Navigation, Bilingual i18n Parity (UA/EN) & Toast Styles
python -m pytest tests/e2e/test_navigation_and_i18n.py -v
```

---

## 4. Visual Headed Execution for Debugging

Run E2E tests with a visual browser window:
```powershell
$env:HEADLESS="0"; python -m pytest tests/e2e/test_navigation_and_i18n.py -v
```
