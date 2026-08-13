# Implementation Plan: Native Desktop File Dialogs for Import/Export

**Branch**: `003-description-native-file-dialogs` | **Date**: 2026-08-13 | **Spec**: [specs/003-native-file-dialogs/spec.md](spec.md)

**Input**: Feature specification from `/specs/003-native-file-dialogs/spec.md`

---

## Summary

Replace manual text `prompt()` inputs for Excel import and export operations with native OS desktop file dialogs using Python's standard library `tkinter.filedialog` (`askopenfilename` and `asksaveasfilename`). Suppress root Tkinter windows using `root.withdraw()` and `root.attributes('-topmost', True)`, expose `open_file_dialog` and `save_file_dialog` RPC endpoints via Eel decorators, and wire the JS frontend to invoke native dialogs on button click.

---

## Technical Context

**Language/Version**: Python 3.14 / HTML5 + Vanilla JS (Eel UI)  
**Primary Dependencies**: `tkinter` (Python stdlib), `eel`, `openpyxl`, `pytest`  
**Storage**: Native Excel `.xlsx` files  
**Testing**: `pytest` (Unit & Integration tests)  
**Target Platform**: Desktop (Windows / macOS / Linux via Eel)  
**Project Type**: Desktop GUI Web Application  
**Performance Goals**: File dialog opens in <300ms, 0 auxiliary background Tk windows  
**Constraints**: Zero external binary dependencies beyond standard library `tkinter.filedialog`  
**Scale/Scope**: All file import and export user actions across the app  

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I (SDD Scope Enforcement)**: PASSED. No source code generated during specify/plan phases.
- **Principle II (OOP & SOLID)**: PASSED. `FileDialogService` provides SRP wrapper for dialog invocation.
- **Principle III (GoF Composite Pattern)**: PASSED. Unchanged existing hierarchy models.
- **Principle IV (Library-First & TDD)**: PASSED. Service wrappers defined with unit tests.
- **Principle V (Self-Contained Excel)**: PASSED. File dialogs use Python stdlib `tkinter.filedialog`.

---

## Project Structure

### Documentation (this feature)

```text
specs/003-native-file-dialogs/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Phase 0 architectural decisions
├── data-model.md        # Phase 1 domain entities & schema
├── quickstart.md        # Phase 1 end-to-end validation guide
├── contracts/
│   └── eel_bridge.json  # Phase 1 Eel RPC API contract
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code Architecture

```text
src/
├── app/
│   ├── eel_bridge.py          # Eel RPC endpoints exposing open_file_dialog and save_file_dialog
│   └── main.py                # App entry point initializing Eel
├── hierarchy_lib/
│   ├── adapters/
│   │   └── excel_adapter.py   # Excel import & horizontal export adapter
│   ├── models/                # Composite pattern domain models
│   └── services/
│       ├── dialog_service.py  # Standalone FileDialogService wrapping tkinter.filedialog
│       ├── forest.py          # Multi-root tree manager
│       └── header_service.py  # Header extraction & sorting
└── web/
    └── js/
        └── app.js             # Wires Import & Export button click events to Eel dialog RPCs

tests/
├── integration/
│   └── test_eel_bridge.py     # Integration tests for Eel bridge RPC endpoints
└── unit/
    └── test_dialog_service.py # Unit tests for FileDialogService (mocked tkinter dialogs)
```

**Structure Decision**: Single project architecture extending existing `hierarchy_lib/services/dialog_service.py` service module and Eel bridge.

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *All principles strictly satisfied without complexity violations.* | *N/A* |
