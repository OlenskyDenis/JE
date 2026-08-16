# Quickstart & Verification: Root Node Controls

**Feature Branch**: `025-root-node-controls`  
**Created**: 2026-08-14

---

## 1. Automated Tests

```powershell
python -m pytest
```

---

## 2. Manual Verification Workflow

1. Start desktop application:
   ```powershell
   python -m src.app.main
   ```
2. Create initial root node via empty state button.
3. Once the tree has at least 1 node:
   - Click `+ Кореневий вузол` in the panel header. Verify modal opens with "Create Node".
   - Submit a new node name (e.g. `Root2`). Verify `Root2` is added at top level.
   - Click the add button at the bottom of the tree canvas.
   - Submit another node (e.g. `Root3`). Verify `Root3` is added as a 3rd top-level node.
4. Toggle language (`UA` / `EN`) and verify all button labels and tooltips update cleanly.
