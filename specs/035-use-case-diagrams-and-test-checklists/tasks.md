# Tasks: Full-Stack Use Case Lifecycle Diagrams & Test Verification Checklists

**Branch**: `035-use-case-diagrams-and-test-checklists` | **Date**: 2026-08-17 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1: Setup & Design

- [x] T001 Initialize dedicated directory `specs/035-use-case-diagrams-and-test-checklists/settings/`
- [x] T002 Define data models, research, contracts, and quickstart documentation under `specs/035-use-case-diagrams-and-test-checklists/`

---

## Phase 2: Entity 1 — Settings Sub-System (Completed)

- [x] T003 [P] [US1] Create Level A Atomic Micro-Lifecycles in `settings/atomic_lifecycles.md`
- [x] T004 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram in `settings/macro_lifecycle_diagram.md`
- [x] T005 [P] [US2] Create Level C Verification Checklist in `settings/verification_checklist.md`

---

## Phase 3: Entity 2 — Node Modal Sub-System (`node_modal/`)

- [x] T006 [P] [US1] Create Level A Atomic Micro-Lifecycles (`ModalContainerLifecycle`, `NameInputValidationLifecycle`, `TypeSelectLifecycle`, `SubmitButtonLifecycle`) in `node_modal/atomic_lifecycles.md`
- [x] T007 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram (Root creation, Add child, Rename, Data type update, Cancel) in `node_modal/macro_lifecycle_diagram.md`
- [x] T008 [P] [US2] Create Level C Verification Checklist (`CHK-NODE-01` to `CHK-NODE-07`) mapped to automated tests in `node_modal/verification_checklist.md`

---

## Phase 4: Entity 3 — Unsaved Changes Modal Sub-System (`unsaved_modal/`)

- [x] T009 [P] [US1] Create Level A Atomic Micro-Lifecycles (`DirtyStateTriggerLifecycle`, `UnsavedModalActionLifecycle`, `PendingActionDispatcherLifecycle`) in `unsaved_modal/atomic_lifecycles.md`
- [x] T010 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram (Dirty trigger on sheet change/file import, Save & continue, Discard, Cancel) in `unsaved_modal/macro_lifecycle_diagram.md`
- [x] T011 [P] [US2] Create Level C Verification Checklist (`CHK-UNS-01` to `CHK-UNS-06`) mapped to automated tests in `unsaved_modal/verification_checklist.md`

---

## Phase 5: Entity 4 — View Mode Switcher Sub-System (`view_modes/`)

- [x] T012 [P] [US1] Create Level A Atomic Micro-Lifecycles (`ViewModeButtonGroupLifecycle`, `MatrixCoordTableLifecycle`, `UniqueLevelChipGroupLifecycle`, `DuplicateSyncHighlightLifecycle`) in `view_modes/atomic_lifecycles.md`
- [x] T013 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram (Tree $\leftrightarrow$ Matrix $\leftrightarrow$ Unique Levels, leaf-first partitioning, synchronized hover) in `view_modes/macro_lifecycle_diagram.md`
- [x] T014 [P] [US2] Create Level C Verification Checklist (`CHK-VIEW-01` to `CHK-VIEW-07`) mapped to automated tests in `view_modes/verification_checklist.md`

---

## Phase 6: Entity 5 — Unified Sidebar Sub-System (`sidebar/`)

- [x] T015 [P] [US1] Create Level A Atomic Micro-Lifecycles (`TabSelectorLifecycle`, `SearchFilterLifecycle`, `CollapseStripLifecycle`, `ResizerSplitterLifecycle`, `CatalogSheetPickerLifecycle`) in `sidebar/atomic_lifecycles.md`
- [x] T016 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram (Tab switch, live query filtering, collapse/expand, resizer drag/reset, catalog sheet switch) in `sidebar/macro_lifecycle_diagram.md`
- [x] T017 [P] [US2] Create Level C Verification Checklist (`CHK-SIDE-01` to `CHK-SIDE-08`) mapped to automated tests in `sidebar/verification_checklist.md`

---

## Phase 7: Entity 6 — Bilingual Localization Sub-System (`i18n/`)

- [x] T018 [P] [US1] Create Level A Atomic Micro-Lifecycles (`LanguageToggleLifecycle`, `DOMTranslationTraversalLifecycle`, `DynamicBadgeTranslatorLifecycle`, `ToastLocaleFormatterLifecycle`) in `i18n/atomic_lifecycles.md`
- [x] T019 [P] [US1] Create Level B Full-Stack Macro Sequence Diagram (Language toggle click, dictionary swap, in-place DOM attribute update, modal strings update, backend error string mapping) in `i18n/macro_lifecycle_diagram.md`
- [x] T020 [P] [US2] Create Level C Verification Checklist (`CHK-I18N-01` to `CHK-I18N-07`) mapped to automated tests in `i18n/verification_checklist.md`

---

## Phase 8: Master Traceability Matrix & Full Quality Gate

- [x] T021 [P] Create Master Traceability Matrix in `traceability_matrix.md` linking all 40+ checklist items across 6 sub-systems to the test suite
- [x] T022 Execute full quality gate test suite (`python scripts/check_all.py --full`) to confirm 100% test pass rate

