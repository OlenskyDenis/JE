# Quickstart & Verification Guide: Feature 033

**Feature Branch**: `033-project-audit-and-hygiene`  
**Date**: 2026-08-17  
**Spec**: [spec.md](spec.md)

---

## 1. Quick Quality Gate Check

Run the comprehensive fast health check (Python compile, JS syntax check, Ruff linter, Pytest test suites):

```powershell
python scripts/check_all.py --quick
```

Expected output:
* `[PASS] All Python source and test files compiled without syntax errors.`
* `[PASS] All JavaScript module files passed syntax check.`
* `[PASS] Ruff static analysis: Zero issues found.`
* `[PASS] All executed test suites passed successfully.`

---

## 2. Modularity & Architecture Guardrail Verification

Run the automated architecture contracts test suite to verify line-count thresholds ($\le 200$ lines), DIP, and dead file prevention:

```powershell
python -m pytest tests/unit/test_architecture_contracts.py -v
```

Expected output:
* `test_file_line_count_thresholds PASSED` (all non-exempt source files $\le 200$ lines)
* `test_domain_models_do_not_import_services_or_adapters PASSED`
* `test_retired_files_do_not_exist PASSED`
* `test_no_retired_rpc_endpoints_in_eel_bridge PASSED`

---

## 3. Frontend Script Integrity & I18n Verification

Verify that all decomposed scripts in `index.html` exist, load cleanly, and contain no broken DOM references:

```powershell
python -m pytest tests/unit/test_frontend_contracts.py -v
```

---

## 4. Full Regression & Playwright E2E Verification

Run the full end-to-end browser test suite to ensure zero UI or workflow regressions:

```powershell
python scripts/check_all.py --full
```
