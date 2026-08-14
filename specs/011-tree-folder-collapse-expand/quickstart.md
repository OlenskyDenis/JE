# Quickstart & Verification Guide: Tree Folder Collapse & Expand

**Feature**: 011-tree-folder-collapse-expand  
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

2. **Import or Build a Multi-Level Tree**:
   - Click "Import Excel" and load a spreadsheet with hierarchical paths (e.g. `Root\Folder\Leaf` or `DB\Tables\Columns`).
   - Confirm all folders render with a chevron toggle icon (`▼`) pointing downwards.

3. **Verify Individual Folder Collapse & Expand**:
   - Click the chevron next to a parent folder.
   - Confirm the chevron rotates to point right (`▶`), and the child subtree collapses (`display: none`).
   - Click the chevron again. Confirm the subtree smoothly re-expands.

4. **Verify State Preservation on Tree Operations**:
   - Collapse one folder.
   - Click the `+` button on a *different* folder to add a new child.
   - Confirm the first folder remains collapsed after the tree re-renders.

5. **Verify Global Expand All / Collapse All**:
   - In the panel header of the Hierarchy Constructor Workspace, click `Collapse All`.
   - Confirm all folder branches across all root trees collapse.
   - Click `Expand All`. Confirm all branches expand simultaneously.

6. **Verify Auto-Expansion on Drag & Drop**:
   - Collapse a folder.
   - Drag a sidebar header onto the collapsed folder center (`NEST_CHILD`).
   - Confirm the folder automatically expands, revealing the newly dropped child inside.
