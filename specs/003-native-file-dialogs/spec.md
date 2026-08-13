# Feature Specification: Native Desktop File Dialogs for Import/Export

**Feature Branch**: `003-description-native-file-dialogs`  
**Created**: 2026-08-13  
**Status**: Draft  

**Input**: User description: "Replace manual text path inputs for Excel import and export with native desktop file dialogs. 1) Import: When the user clicks the Excel Import button, open a native OS file selection dialog (using Python's tkinter.filedialog.askopenfilename) filtered for .xlsx files. Once selected, return the absolute file path to the frontend and proceed with sheet loading. 2) Export: When exporting, open a native save file dialog (asksaveasfilename) to let the user visually choose the directory and filename to save their reorganized headers."

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **SDD Scope Enforcement**: No source code is generated during this specification phase.
- **OOP & SOLID Design**: Dialog services are decoupled from domain logic via standalone bridge adapters.
- **Library-First & TDD**: File dialog service wrappers are defined with unit and contract tests.
- **Self-Contained Excel**: Native OS file dialog integration requires no external heavy dependencies beyond standard library `tkinter.filedialog`.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Native OS Open File Dialog for Excel Import (Priority: P1)

As a database designer or data analyst, I want a native OS file selection dialog to open when I click "Import Excel", so that I can visually browse folders and select my `.xlsx` file without typing manual text paths.

**Why this priority**: Eliminates friction and user error associated with typing raw absolute file paths in text prompts.

**Independent Test**: Can be tested by clicking the "Import Excel" button, confirming the OS file picker opens filtered for `.xlsx` files, selecting a file, and verifying that the file path is returned to load sheet headers.

**Acceptance Scenarios**:

1. **Given** the application running in Eel desktop window, **When** the user clicks the "Import Excel" button, **Then** a native OS file open dialog appears filtered for Excel files (`*.xlsx`).
2. **Given** the open file dialog displayed on screen, **When** the user selects an `.xlsx` file and clicks Open, **Then** the dialog closes, the absolute path is returned to the backend, and sheet headers are loaded.
3. **Given** the open file dialog displayed on screen, **When** the user clicks Cancel or closes the dialog, **Then** no file is imported and the application state remains unchanged without error messages.

---

### User Story 2 - Native OS Save File Dialog for Excel Export (Priority: P2)

As a data manager, I want a native OS save file dialog to open when I click "Export Excel", so that I can visually choose the target directory and filename for saving my reorganized Excel header structure.

**Why this priority**: Provides a standard, user-friendly file save experience with folder navigation and default file extension handling.

**Independent Test**: Can be tested by building a tree, clicking "Export Excel", selecting a destination folder and filename in the save dialog, and verifying that the output file is created at the chosen path.

**Acceptance Scenarios**:

1. **Given** a constructed tree structure ready for export, **When** the user clicks the "Export Excel" button, **Then** a native OS save file dialog opens pre-populated with a default filename (`reorganized_headers_export.xlsx`) and `.xlsx` filter.
2. **Given** the save file dialog, **When** the user selects a directory, enters a filename, and clicks Save, **Then** the dialog closes and the backend writes the horizontal Row 1 leaf path strings into the specified file.
3. **Given** the save file dialog, **When** the user clicks Cancel or closes the dialog, **Then** the export operation is safely aborted without creating or modifying files.

---

### Edge Cases

- **Hidden Tkinter Root Window**: The `tkinter` root window must be hidden (`withdraw()`) so no blank secondary desktop window flashes or stays open behind the main application window.
- **Dialog Cancellation**: Canceling an open or save dialog returns `{ "cancelled": True, "file_path": None }` cleanly without throwing Python exceptions or JavaScript errors.
- **Invalid/Non-Existent File Selected**: If a non-existent file path is somehow passed, the system returns a user-friendly error toast.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace manual text path `prompt()` popups for Excel import and export with native OS file dialogs using Python `tkinter.filedialog`.
- **FR-002**: System MUST expose an Eel RPC endpoint `open_file_dialog()` that opens `askopenfilename` filtered for `[("Excel Files", "*.xlsx"), ("All Files", "*.*")]` and returns the selected absolute path or cancellation status.
- **FR-003**: System MUST expose an Eel RPC endpoint `save_file_dialog(default_name)` that opens `asksaveasfilename` with `defaultextension=".xlsx"` and returns the selected destination path or cancellation status.
- **FR-004**: System MUST suppress the root `tkinter.Tk()` window using `withdraw()` and `destroy()` to prevent background window artifacts during dialog invocations.
- **FR-005**: Frontend MUST handle dialog cancellation gracefully, closing modal/action states without triggering error notices.

### Key Entities

- **File Dialog Request**: Parameters specifying dialog mode (`open` or `save`), file types filter (`*.xlsx`), default filename, and window title.
- **File Dialog Result**: Result object containing `cancelled` (`bool`) and `file_path` (`str` or `None`).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Native file dialog opens in under 300 milliseconds after clicking the Import or Export button.
- **SC-002**: 100% of dialog cancellations exit cleanly without throwing errors or corrupting app state.
- **SC-003**: 0 auxiliary Tkinter root windows appear on screen during file dialog operations.

---

## Assumptions

- Standard library `tkinter` is available in the target Python runtime environment.
- Native file dialogs run synchronously on the host operating system thread via Eel RPC calls.
- Web UI handles returning path strings seamlessly.
