# Quickstart Validation Guide: Row-1 Column Data Type Inference

**Feature Branch**: `021-excel-data-types-bug`  
**Spec**: [specs/021-excel-data-types-bug/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Automated Test Suite Execution

Run all automated unit and integration tests across the project:

```powershell
python -m pytest
```

Expected Outcome: All 57+ unit and integration tests pass with 0 failures.

---

## 2. Unit Testing Specific Components

To run tests specifically for Excel column format inspection:

```powershell
python -m pytest tests/unit/test_excel_adapter.py -k "test_infer_column_types_from_excel_cells or test_read_row1_headers_and_types"
```

To run Eel bridge integration tests:

```powershell
python -m pytest tests/integration/test_eel_bridge.py
```

---

## 3. End-to-End Manual Verification Scenario

1. **Launch Desktop Application**:
   ```powershell
   python -m src.app.main
   ```
2. **Import Test Excel File**:
   - Click `Import Excel` and select a file where columns have distinct formatting set in Excel (e.g. `Currency`, `Date`, `Integer`, `Percentage`, `Text`).
3. **Verify Canvas Tree Badges**:
   - Verify leaf element nodes show correct colored `.node-type-badge` badges corresponding to the Excel column formats.
4. **Verify Sidebar Catalog**:
   - Verify sidebar catalog items show `.header-type-tag` pills matching the detected types.
5. **Verify Drag-and-Drop**:
   - Drag a `Date` item from the sidebar catalog into the workspace canvas.
   - Verify the newly created node receives `data_type="Date"` and displays `[Date]`.
6. **Verify Exported Template**:
   - Click `Export Excel` or `Save Template`.
   - Open the generated template file and verify Row 1 cell number formats match the leaf element types.
