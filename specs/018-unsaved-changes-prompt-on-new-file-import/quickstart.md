# Quickstart & Verification Guide: Unsaved Changes Protection on New File Import

**Feature**: 018-unsaved-changes-prompt-on-new-file-import  
**Date**: 2026-08-14  

---

## 1. Automated Test Suite Verification

Run the full pytest suite:

```powershell
python -m pytest
```

---

## 2. End-to-End Manual Verification Workflow

### Step 1: Launch Application
```powershell
python -m src.app.main
```

### Step 2: Direct Import on Clean Workspace
1. With a fresh empty workspace (`isDirty == false`), click **Import Excel**.
2. Confirm the native open file picker opens immediately. Select `FileA.xlsx`.

### Step 3: Modify Hierarchy & Attempt Import
1. Add custom child nodes to the workspace on `FileA` (`isDirty` becomes `true`).
2. Click **Import Excel**.
3. Confirm that the open file picker does NOT open immediately. Instead, the **Unsaved Changes** modal appears.
4. Confirm the modal displays:
   - Message: *"You have unsaved changes in your current session. Save your changes to a template file before importing a new file?"*
   - Buttons: `[Save Template & Import]`, `[Discard & Import]`, `[Cancel]`.

### Step 4: Verify Cancel Action
1. In the modal, click **Cancel**.
2. Confirm the modal closes, and the canvas remains unchanged with all nodes intact (`isDirty == true`).

### Step 5: Verify Save & Import Flow
1. Click **Import Excel** again.
2. Click **Save Template & Import**.
3. In the save dialog, save to `Шаблон_FileA.xlsx`.
4. Confirm:
   - Template file `Шаблон_FileA.xlsx` is saved to disk.
   - The open file picker automatically appears to select the new file!
5. Select `FileB.xlsx` and verify `FileB` loads cleanly.

### Step 6: Verify Discard & Import Flow
1. On `FileB`, add a node (`isDirty == true`).
2. Click **Import Excel**.
3. In the modal, click **Discard & Import**.
4. Confirm the open file picker appears immediately. Select `FileA.xlsx`.
5. Verify `FileA` loads cleanly without error.
