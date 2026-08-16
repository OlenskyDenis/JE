# Quickstart Guide: Running Playwright E2E Tests

**Feature Branch**: `031-playwright-e2e-testing`  
**Created**: 2026-08-16  
**Status**: Ready  

---

## 1. Installation

Install Playwright and browser binaries:
```powershell
pip install pytest-playwright
playwright install chromium
```

---

## 2. Running E2E Test Suites

Run all E2E browser tests headlessly:
```powershell
python -m pytest tests/e2e/ -v
```

Run specific test modules:
```powershell
python -m pytest tests/e2e/test_navigation_and_i18n.py -v
python -m pytest tests/e2e/test_tree_crud_and_modals.py -v
python -m pytest tests/e2e/test_drag_and_drop.py -v
python -m pytest tests/e2e/test_excel_matrix_and_unique_levels.py -v
python -m pytest tests/e2e/test_settings_and_persistence.py -v
python -m pytest tests/e2e/test_sidebar_and_resizer.py -v
```

Run both backend unit tests and frontend E2E browser tests:
```powershell
python -m pytest
```
