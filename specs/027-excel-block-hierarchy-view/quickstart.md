# Quickstart & Verification Guide: Excel Block Hierarchy View (Feature 027)

**Feature Branch**: `027-excel-block-hierarchy-view`  
**Created**: 2026-08-16  
**Status**: Completed  

---

## 1. Automated Verification

Run all unit and integration tests via:
```powershell
python -m pytest
```

Ensure all tests pass with zero errors and no regressions.

---

## 2. Manual End-to-End Verification Steps

### Step 1: Launch Application
```powershell
python -m src.app.main
```

### Step 2: Empty State Verification
1. Launch app on an empty workspace.
2. In the workspace header, verify the new view mode segmented switcher: `[ Дерево | Блоки Excel ]`.
3. Click `Блоки Excel`.
4. Verify that the workspace displays a clean, localized empty state message.

### Step 3: Multi-Level Block Rendering & Colspan Calculation
1. Switch back to `Дерево`.
2. Click `Створити кореневий вузол` -> Name: `Finance`.
3. Under `Finance`, add two folders: `Q1` and `Q2`.
4. Under `Q1`, add two leaf elements: `Revenue` (`Currency`) and `Expenses` (`Currency`).
5. Under `Q2`, add one leaf element: `Revenue` (`Currency`).
6. Add a standalone root element: `Notes` (`Text`).
7. Switch to `Блоки Excel`.
8. Verify the block matrix:
   - **Column Coordinate Header**: Displays `A`, `B`, `C`, `D` above the 4 columns.
   - **Tier 0 (Roots)**:
     - `Finance` block spans 3 columns (`A` to `C`, `colspan=3`).
     - `Notes` block spans 1 column (`D`, `colspan=1`) and extends down all 3 vertical rows (`rowspan=3`).
   - **Tier 1 (Sub-folders)**:
     - `Q1` spans 2 columns (`A` and `B`, `colspan=2`).
     - `Q2` spans 1 column (`C`, `colspan=1`).
   - **Tier 2 (Leaves)**:
     - `Revenue` (Col A, `colspan=1`), `Expenses` (Col B, `colspan=1`), `Revenue` (Col C, `colspan=1`).
9. Hover over each block:
   - Verify that the native tooltip displays the full path, data type, and column span.

### Step 4: Real-Time Synchronization & Multi-Sheet Switching
1. Import a multi-sheet Excel file.
2. Switch between sheets using `#activeSheetSelector`.
3. Verify that the Excel Block Matrix instantly reflects each sheet's unique hierarchy.
4. Modify nodes (rename, add child, change data type) in Tree view and switch to Excel Blocks view: verify changes are immediately reflected.
5. In Settings, change the delimiter to `/` or `::`: verify hover tooltips and paths in Excel Blocks view update in real time.

### Step 5: Bilingual Localization & Persistence
1. Switch language between `UA` and `EN`.
2. Verify all switcher buttons, labels, tooltips, and empty states update instantly.
3. Reload the application: verify the previously chosen view mode is remembered.
