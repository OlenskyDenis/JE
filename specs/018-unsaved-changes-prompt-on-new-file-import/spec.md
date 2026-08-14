# Feature Specification: Unsaved Changes Protection on New File Import

**Feature Branch**: `018-unsaved-changes-prompt-on-new-file-import`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "When importing a new Excel file, if there have been any changes, it should prompt the user to save the existing changes"

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean State Architecture)**:
  - Global Session Protection: Intercepts the `Import Excel` action (`#btnImportExcel`) whenever `isDirty == true`.
  - Non-Destructive Workflow: Prevents existing tree nodes and multi-sheet modifications from being wiped out without explicit user confirmation.
  - Template Synchronization: Integrates with `save_template_sync`, supporting 1-click updates to bound template files or initial template creation prior to loading a new workbook session.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates cancel paths, file picker cancellation after saving, failed imports, and scratch sessions with unsaved nodes.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Data Loss Prevention when Importing a New File (Priority: P1) 🎯 MVP

As a user who has constructed or modified hierarchy trees in the current session, I want to be prompted to save my unsaved changes before a new Excel file is imported, and upon saving, immediately and seamlessly open the file picker for the new file, so that I never accidentally lose my work and experience zero friction.

**Why this priority**: Prevents catastrophic data loss when clicking "Import Excel" while having active, unsaved modifications, while providing a seamless transition to selecting the new file.

**Independent Test**:
1. Open the app and create or modify nodes in the workspace (`isDirty == true`).
2. Click the toolbar button **Import Excel**.
3. Verify that the file dialog does NOT immediately open; instead, an **Unsaved Changes** modal appears.
4. Verify the modal displays:
   - Message: *"You have unsaved changes in your current workspace session. Do you want to save your changes to a template file before importing a new file?"*
   - Buttons: `[Save/Update & Import]`, `[Discard & Import]`, `[Cancel]`.
5. Click **Cancel**:
   - Verify the modal closes and the workspace remains exactly as it was with all nodes intact.
6. Click **Import Excel** again and click **Save/Update & Import**:
   - Verify changes are saved to the template, and immediately afterward, the native open file picker automatically appears to select the new file.

**Acceptance Scenarios**:

1. **Given** a session with unsaved changes (`isDirty == true`), **When** the user clicks `Import Excel`, **Then** the Unsaved Changes confirmation modal is displayed before any file dialog opens.
2. **Given** the modal prompt, **When** the user clicks `Cancel`, **Then** the import process is aborted and the current session is preserved.
3. **Given** the modal prompt, **When** the user clicks `Discard & Import`, **Then** dirty state is cleared and the file picker dialog opens immediately to select the new file.
4. **Given** a bound template file (`currentTemplatePath`) and unsaved changes, **When** the user clicks `Update Template & Import`, **Then** the existing template is synced in 1 click, after which the open file picker dialog immediately and automatically appears.
5. **Given** no template file bound yet and unsaved changes, **When** the user clicks `Save Template & Import`, **Then** the OS save dialog opens to save `Шаблон_<name>.xlsx`, and upon successful save, the open file picker dialog immediately and automatically appears.
6. **Given** a clean session without unsaved changes (`isDirty == false`), **When** the user clicks `Import Excel`, **Then** the file picker dialog opens directly without showing the modal.

---

## Edge Cases

- **User Cancels File Picker After Saving**: If the user saves their changes (`Save Template & Import`) but then cancels the open file dialog, their previous changes remain safely saved, `isDirty` becomes `false`, and the current workspace remains loaded.
- **Empty / Fresh Session**: When the workspace is completely empty or newly imported with `isDirty == false`, clicking `Import Excel` immediately opens the file picker.
- **Scratch Workspace with Custom Nodes**: If a user built a hierarchy from scratch without importing a file, clicking `Import Excel` still recognizes `isDirty == true` and prompts to save.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Clicking the **Import Excel** button (`#btnImportExcel`) MUST check `isDirty`. If `isDirty == true`, it MUST intercept the click and display the Unsaved Changes modal.
- **FR-002**: If `isDirty == false`, clicking **Import Excel** MUST open the native OS file picker directly.
- **FR-003**: The Unsaved Changes modal for import MUST provide 3 clear actions:
  - `[Save/Update Template & Import]`: Saves current session across all modified sheets, then opens the file dialog to import.
  - `[Discard & Import]`: Resets `isDirty` and opens the file dialog to import.
  - `[Cancel]`: Aborts the import operation completely.
- **FR-004**: If `currentTemplatePath` is bound, the save action MUST perform a 1-click update via `save_template_sync(currentTemplatePath)` without opening the save file dialog.
- **FR-005**: If no template file is bound, the save action MUST prompt with `save_file_dialog` before proceeding with the import.
- **FR-006**: All automated test suites in `pytest` MUST continue to pass with 100% pass rate (`python -m pytest`).
- **FR-007**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document the import dirty state protection lifecycle.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0% accidental data loss when importing new files over modified sessions.
- **SC-002**: 100% of cancellation and discard pathways return the UI to a consistent, responsive state.
- **SC-003**: 100% automated test suite pass rate (`python -m pytest`).

---

## Assumptions

- Reuses the existing `#unsavedModal` component by dynamically tailoring the message and action handlers based on the trigger context (`switch_sheet` vs `import_file`).
