# Quickstart & Verification Guide: Unique Level Hierarchy View (Feature 028)

**Feature Branch**: `028-unique-level-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  

---

## 1. Automated Verification

Run all unit, integration, and frontend contract tests via:
```powershell
python -m pytest
```

Ensure all tests pass with zero errors and 100% contract compliance.

---

## 2. Manual End-to-End Verification Steps

### Step 1: Launch Application
```powershell
python -m src.app.main
```

### Step 2: 3-Way View Switcher Verification
1. Inspect the workspace header toolbar.
2. Verify the segmented switcher has 3 buttons: `[ Дерево | Блоки Excel | Унікальні за рівнями ]`.
3. Click `Унікальні за рівнями`.
4. On an empty tree, verify the empty state message.

### Step 3: Level Deduplication & Match Highlighting
1. Switch to `Дерево` and create the following nodes:
   - `Finance` (Root) -> `Revenue` (Leaf), `Expenses` (Leaf), `ID` (Leaf)
   - `Operations` (Root) -> `Revenue` (Leaf), `Costs` (Leaf)
   - `ID` (Root, Standalone Leaf)
2. Switch to `Унікальні за рівнями`.
3. Verify the level rows:
   - **Рівень 0 (Корені)**:
     - Chips: `Finance`, `Operations`, `ID` (3 unique chips).
     - `ID` has a Cross-Match badge `[Збіг: Рівні 0, 1]`.
   - **Рівень 1**:
     - Chips: `Revenue` (`×2`), `Expenses` (`×1`), `Costs` (`×1`), `ID` (`×1`).
     - `Revenue` has occurrence count `×2`.
     - `ID` has Cross-Match badge `[Збіг: Рівні 0, 1]`.
4. Hover over `ID` on Level 0:
   - Verify that `ID` on Level 1 also instantly lights up with an amber/cyan glowing highlight border.
5. Hover over `Revenue` on Level 1:
   - Verify the tooltip displays both absolute paths: `Finance\Revenue` and `Operations\Revenue`.

### Step 4: Real-Time Synchronization & Localization
1. Switch language between `UA` and `EN`:
   - Verify all level titles, badges, and tooltips update to English.
2. In Settings, change the delimiter: verify tooltips update with the new delimiter.
3. Reload the application: verify `Унікальні за рівнями` preference is restored from `localStorage`.
