# Quickstart: Validating Feature 035 Lifecycle Diagrams & Checklists

**Feature**: 035-use-case-diagrams-and-test-checklists  
**Date**: 2026-08-17  

---

## 1. Validating Mermaid Diagrams

Open the markdown documents in VS Code or any GitHub markdown previewer to verify syntax correctness:
- `specs/035-use-case-diagrams-and-test-checklists/settings/atomic_lifecycles.md`
- `specs/035-use-case-diagrams-and-test-checklists/settings/macro_lifecycle_diagram.md`

---

## 2. Executing Automated Tests Mapped to the Checklist

Run all tests referenced in `settings/verification_checklist.md`:

```powershell
# 1. Targeted E2E Settings test suite
python -m pytest tests/e2e/test_settings_and_preferences.py -v

# 2. Targeted Unit Settings Service test suite
python -m pytest tests/unit/test_settings_service.py -v

# 3. Targeted Matrix Test for Settings Flow
python -m pytest tests/e2e/test_automated_interaction_matrix.py -k "flow_settings_modal_delimiter_change" -v
```

---

## 3. Full Quality Gate Verification

```powershell
python scripts/check_all.py --quick
```
