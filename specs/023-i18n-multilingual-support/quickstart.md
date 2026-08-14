# Quickstart & Verification Guide: Multilingual Localization

**Feature Branch**: `023-i18n-multilingual-support`  
**Spec**: [specs/023-i18n-multilingual-support/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Automated Test Suite Execution

Verify test baseline and Python RPC compatibility:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Walkthrough

1. **Launch Desktop Application**:
   ```powershell
   python -m src.app.main
   ```
2. **Verify Default Ukrainian (`uk`) Locale**:
   - Verify header title displays `"Конструктор ієрархії баз даних"`.
   - Verify buttons display `"Імпорт Excel"`, `"Експорт Excel"`.
   - Verify empty state text is in Ukrainian (`"Робоча область порожня"`).
   - Verify language toggle has `UA` selected as active.
3. **Toggle to English (`EN`)**:
   - Click `EN` on the toolbar switcher.
   - Verify all static text, tabs (`Header Catalog`, `Export Preview`), placeholders (`Filter headers in real-time...`), and counter badges immediately switch to English without page reload.
4. **Interact with Workspace**:
   - Add a root node, child node, edit a node.
   - Verify modal dialogs and toasts appear in English.
5. **Toggle back to Ukrainian (`UA`)**:
   - Click `UA`.
   - Verify modal titles, action button tooltips, node actions, and counters update to Ukrainian while existing created tree nodes remain unchanged.
6. **Restart Application (Persistence Test)**:
   - Close and restart the desktop app.
   - Verify the app boots with the last active language.
