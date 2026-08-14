# Quickstart & Verification Guide: Empty-State Root Creation & Header Cleanup

**Feature**: 009-remove-redundant-add-root-button  
**Date**: 2026-08-14  

## 1. Automated Test Verification

Run all test suites to confirm 0 regressions:

```powershell
python -m pytest
```

## 2. End-to-End Manual Verification Workflow

1. **Start the Application**:
   ```powershell
   python -m src.app.main
   ```

2. **Verify Clean Workspace Header**:
   - Inspect the top header of "Hierarchy Constructor Workspace".
   - Confirm `#btnAddRoot` is absent and only the title and `0 Nodes` badge are visible.

3. **Verify Empty-State Actionable Button**:
   - In the center of the empty workspace canvas, verify the presence of the `+ Create Root Node` button (`#btnCreateRootEmpty`).
   - Click the button. Confirm the creation modal opens with the title "Create Root Node".
   - Type `MyNewDatabase` and press Enter / Submit.
   - Confirm the root node appears on canvas and `#treeEmptyState` hides immediately.

4. **Verify Excel Import Flow**:
   - Click "Import Excel" and load an `.xlsx` file.
   - Confirm the auto-generated tree populates the canvas seamlessly.
