# Implementation Plan: Unsaved Changes Protection on New File Import

**Branch**: `018-unsaved-changes-prompt-on-new-file-import` | **Date**: 2026-08-14 | **Spec**: [specs/018-unsaved-changes-prompt-on-new-file-import/spec.md](spec.md)

**Input**: Feature specification from `/specs/018-unsaved-changes-prompt-on-new-file-import/spec.md`

---

## Summary

Extend the unsaved changes state machine to intercept the **Import Excel** button (`#btnImportExcel`) whenever `isDirty == true`. Prompt the user with context-aware confirmation choices (`Save / Update Template & Import`, `Discard & Import`, `Cancel`), protecting against accidental session overwrite and seamlessly opening the native open file picker immediately upon saving or discarding.

---

## Technical Context

**Language/Version**: Vanilla JavaScript ES6+ (Frontend State Controller), HTML5, CSS3  
**Testing**: `pytest` automated test suite (`python -m pytest`)  
**Target Platform**: Desktop GUI (Windows / Chromium via Eel)  
**Constraints**: 0% data loss when importing over modified sessions, seamless file picker presentation post-save, 0 regressions in sheet-switching dirty state checks.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. Spec and Plan authored prior to code changes.
- **Principle II (OOP & Clean State Architecture)**: PASSED. State machine unifies modal prompts via polymorphic `pendingAction: { type: 'switch_sheet' | 'import_file', targetSheet?: string }`.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: PASSED. Consulted [`.specify/system_map.md`](../../.specify/system_map.md).
- **Principle VII (Proactive Red Teaming & Zero-Data Stress Testing)**: PASSED. Validated import cancellation after saving, failed save recovery, and discard transitions.

---

## Project Structure

### Documentation (this feature)

```text
specs/018-unsaved-changes-prompt-on-new-file-import/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # State machine unification & dialog flow decisions
├── quickstart.md        # Verification guide
└── checklists/
    └── requirements.md  # Quality & compliance checklist
```

### Source Code Architecture

```text
src/
└── web/
    └── js/
        └── app.js       # pendingAction state machine handling both switch_sheet and import_file
```

---

## Implementation Sequence

### Phase 1: Controller State Machine Refactoring (`src/web/js/app.js`)
1. Introduce `this.pendingAction = null` replacing `this.pendingSwitchSheetName`.
2. Extract `this.promptOpenAndImportFile()` helper for opening the native OS file picker and triggering `handleImportExcelFile`.
3. Update `#btnImportExcel` click event:
   - If `this.isDirty == true`: set `this.pendingAction = { type: 'import_file' }`, configure modal messages and buttons (`Save/Update Template & Import`, `Discard & Import`), and display `#unsavedModal`.
   - If `this.isDirty == false`: call `this.promptOpenAndImportFile()` directly.
4. Update `this.activeSheetSelector` change event:
   - If `this.isDirty == true`: set `this.pendingAction = { type: 'switch_sheet', targetSheet: selectedSheet }`, configure modal messages and buttons (`Save/Update Template & Switch`, `Discard & Switch`), and display `#unsavedModal`.
5. Update `btnUnsavedDiscard` and `btnUnsavedSave` event handlers to branch seamlessly on `this.pendingAction.type`.

### Phase 2: System Map Sync & Quality Assurance
1. Update [`.specify/system_map.md`](../../.specify/system_map.md).
2. Run full pytest suite `python -m pytest` (48/48 tests).
3. Execute end-to-end manual verification per `quickstart.md`.

---

## Complexity Tracking

| Dimension | Risk / Effort | Mitigation |
|---|---|---|
| State Machine Generalization | Low | Reuses existing `#unsavedModal` with clear action type discrimination |
| Chained Dialog UX | Low | `promptOpenAndImportFile` invoked directly in save success callback |
