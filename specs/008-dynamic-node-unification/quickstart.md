# Quickstart & Verification Guide: Dynamic Node Unification

**Feature**: 008-dynamic-node-unification  
**Date**: 2026-08-14  

## 1. Automated Test Verification

Run all unit and integration tests:

```powershell
python -m pytest tests/unit/test_composite.py
python -m pytest
```

## 2. Manual Verification in Desktop UI

1. **Start the Application**:
   ```powershell
   python -m src.app.main
   ```

2. **Test Dynamic Upgrade (Leaf -> Folder)**:
   - Click **Add Root Node**, enter `MyRoot`.
   - Verify `MyRoot` displays with a leaf icon (0 children).
   - Click `+` (Add Child) on `MyRoot`, enter `ChildA`.
   - Verify `MyRoot` instantly upgrades to a folder icon and displays `ChildA` nested underneath.

3. **Test Dynamic Downgrade (Folder -> Leaf)**:
   - Click the Delete (trash) icon on `ChildA`.
   - Verify `MyRoot` instantly reverts to a leaf icon.

4. **Test Universal Drag-and-Drop Nesting**:
   - Drag a header from the sidebar directly onto a leaf node's center area (`NEST_CHILD`).
   - Verify the leaf node accepts the drop, becomes a folder, and nests the dropped header inside.
