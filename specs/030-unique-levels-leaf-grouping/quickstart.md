# Quickstart & Verification Guide: Leaf-First Partitioning (Feature 030)

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Created**: 2026-08-16  
**Status**: Ready  

---

## 1. Automated Verification
Run all automated test suites to verify integrity:
```powershell
python -m pytest
```

---

## 2. Manual Verification Walkthrough

1. Launch application:
   ```powershell
   python -m src.app.main
   ```
2. In `Tree View` (`Дерево`), build a tree with both leaf and branch roots:
   - Root 1: `ID` (leaf root, no children)
   - Root 2: `Status` (leaf root, no children)
   - Root 3: `Finance` (branch root) -> `Revenue` (leaf), `Expenses` (leaf)
   - Root 4: `Operations` (branch root) -> `Costs` (leaf), `Revenue` (leaf)
3. Switch to `Unique by Levels` (`Унікальні за рівнями`).
4. Verify **Рівень 0 (Корені)**:
   - First block displays: `ID`, `Status` (Leaf group).
   - Paragraph separator is visible.
   - Second block displays: `Finance`, `Operations` (Branch group).
5. Verify **Рівень 1**:
   - Displays `Costs`, `Expenses`, `Revenue` (all leaves, no empty branch group or dangling divider).
6. Double-click any chip to verify the Node Edit modal opens with batch notice.
7. Hover over `Revenue` on Level 1 to verify hover sync highlights both paths.
