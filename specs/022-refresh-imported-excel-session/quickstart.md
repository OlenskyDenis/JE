# Quickstart Validation Guide: Refresh Excel Session

**Feature Branch**: `022-refresh-imported-excel-session`  
**Spec**: [specs/022-refresh-imported-excel-session/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Automated Test Execution

Run the complete test suite including integration tests for `refresh_excel_session`:

```powershell
python -m pytest tests/integration/test_eel_bridge.py -k "test_eel_refresh_excel_session"
```

Run the entire automated test suite:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Walkthrough

1. **Launch Desktop Application**:
   ```powershell
   python -m src.app.main
   ```
2. **Initial State (No Session)**:
   - Click the Refresh button in the top toolbar.
   - Verify warning toast: `"No active Excel session loaded to refresh."`
3. **Import File**:
   - Import an Excel file `Sample.xlsx`.
4. **External Modification**:
   - Open `Sample.xlsx` in Excel or an editor; add a column `NewCol` with currency formatting.
   - Save `Sample.xlsx`.
5. **Click Refresh**:
   - In the application, click `#btnRefresh`.
   - Verify success toast: `"Refreshed Excel session from 'Sample.xlsx'."`
   - Verify `NewCol [Currency]` immediately appears in the sidebar catalog and tree.
6. **Dirty State Protection**:
   - Rename a node in the tree to create unsaved changes.
   - Click `#btnRefresh`.
   - Verify Unsaved Changes modal appears asking to save or discard before refreshing.
