# Research & Architectural Decisions: Unsaved Changes Protection on New File Import

**Feature**: 018-unsaved-changes-prompt-on-new-file-import  
**Date**: 2026-08-14  

---

## Decision 1: Unified `pendingAction` State Structure

- **Context**: In Feature 015 & 016, `#unsavedModal` only tracked `this.pendingSwitchSheetName`. When the user wanted to import a new file over unsaved work, there was no interception mechanism.
- **Decision**: Generalize the dirty state trigger into a unified `pendingAction` object:
  ```typescript
  type PendingAction =
    | { type: 'switch_sheet'; targetSheet: string }
    | { type: 'import_file' };
  ```
- **Rationale**:
  1. **Single Modal Reusability**: Prevents DOM bloat by reusing `#unsavedModal` with dynamic button labels (`& Switch` vs `& Import`).
  2. **Predictable State Transitions**: Centralizes all post-save and post-discard execution in one well-defined controller handler.

---

## Decision 2: Seamless Post-Save Import Trigger

- **Context**: When a user selects `Save/Update Template & Import`, they want to preserve their work and immediately proceed to choosing their new file.
- **Decision**: Upon successful completion of `save_template_sync`, automatically invoke `this.promptOpenAndImportFile()`.
- **Rationale**: Eliminates unnecessary friction; the user does not have to click "Import Excel" a second time after saving.
