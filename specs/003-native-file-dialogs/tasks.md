# Task Breakdown: Native Desktop File Dialogs for Import/Export

**Feature**: `003-native-file-dialogs`  
**Branch**: `003-description-native-file-dialogs`  
**Spec**: [specs/003-native-file-dialogs/spec.md](spec.md)  
**Plan**: [specs/003-native-file-dialogs/plan.md](plan.md)  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Service module placeholders

- [x] T001 Create `FileDialogService` in `src/hierarchy_lib/services/dialog_service.py` and test file in `tests/unit/test_dialog_service.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories begin

- [x] T002 [P] Implement `FileDialogService.ask_open_file` and `ask_save_file` using `tkinter.filedialog` with `root.withdraw()`, `root.attributes('-topmost', True)`, and `root.destroy()` in `src/hierarchy_lib/services/dialog_service.py`

---

## Phase 3: User Story 1 - Native OS Open File Dialog for Excel Import (Priority: P1) 🎯 MVP

**Goal**: Open native OS file picker (`askopenfilename`) on "Import Excel" click, returning selected `.xlsx` path or cancellation state.

**Independent Test**: Click "Import Excel" button, confirm native OS open dialog opens filtered for `*.xlsx` files, select file, and verify path is passed to sheet loader.

### Tests for User Story 1
- [x] T003 [P] [US1] Write unit tests for `ask_open_file` with mocked `tkinter.filedialog` in `tests/unit/test_dialog_service.py`

### Implementation for User Story 1
- [x] T004 [US1] Expose `open_file_dialog` Eel RPC endpoint in `src/app/eel_bridge.py` (depends on T002, T003)
- [x] T005 [US1] Wire Import Excel button in `src/web/js/app.js` to call `eel.open_file_dialog()` instead of manual text `prompt()`

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently (MVP).

---

## Phase 4: User Story 2 - Native OS Save File Dialog for Excel Export (Priority: P2)

**Goal**: Open native OS save file dialog (`asksaveasfilename`) on "Export Excel" click, returning chosen target path or cancellation state.

**Independent Test**: Click "Export Excel" button, confirm native OS save dialog opens pre-filled with `.xlsx` default extension, choose path, and verify file is written.

### Tests for User Story 2
- [x] T006 [P] [US2] Write unit tests for `ask_save_file` with mocked `tkinter.filedialog` in `tests/unit/test_dialog_service.py`

### Implementation for User Story 2
- [x] T007 [US2] Expose `save_file_dialog` Eel RPC endpoint in `src/app/eel_bridge.py` (depends on T002, T006)
- [x] T008 [US2] Wire Export Excel button in `src/web/js/app.js` to call `eel.save_file_dialog()` instead of manual text `prompt()`

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Integration testing and quickstart validation

- [x] T009 [P] Write integration tests for `open_file_dialog` and `save_file_dialog` RPC endpoints in `tests/integration/test_eel_bridge.py`
- [x] T010 Run complete test suite (`python -m pytest`) to confirm all tests pass cleanly

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion. BLOCKS user story implementations.
- **User Story 1 (Phase 3)**: Depends on Foundational phase.
- **User Story 2 (Phase 4)**: Depends on Foundational phase.
- **Polish (Phase 5)**: Depends on completion of user stories.

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1 & Phase 2.
2. Complete Phase 3 (User Story 1).
3. Test native file open dialog for Excel import independently.

### Incremental Delivery
1. Deliver US1 (Native Open Dialog for Import).
2. Deliver US2 (Native Save Dialog for Export).
