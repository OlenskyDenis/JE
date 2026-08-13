# Research & Architectural Decisions: Native Desktop File Dialogs

**Feature**: `003-native-file-dialogs`  
**Date**: 2026-08-13  
**Status**: Complete  

---

## Technical Context & Research Summary

### 1. Backend Native Dialog Library Choice
- **Decision**: Use Python standard library `tkinter.filedialog` (`askopenfilename` and `asksaveasfilename`).
- **Rationale**: Built into standard Python installation across Windows, macOS, and Linux without adding third-party dependencies (keeps project lightweight and self-contained).
- **Alternatives Considered**:
  - `wxPython` / `PyQt`: Rejected due to heavy external binary dependencies.
  - HTML5 `<input type="file">`: Rejected because browser security models do not expose absolute file system paths or native save file dialogs.

---

### 2. Tkinter Root Window Suppression (`root.withdraw()`)
- **Decision**: Create an invisible `tkinter.Tk()` instance, apply `root.withdraw()`, set `root.attributes('-topmost', True)`, invoke the dialog, and immediately call `root.destroy()`.
- **Rationale**: `root.withdraw()` hides the main blank Tkinter frame so no background window flashes behind the Eel window. `attributes('-topmost', True)` ensures the native OS file picker appears in front of the Eel Chromium window.
- **Implementation Pattern**:
  ```python
  import tkinter as tk
  from tkinter import filedialog

  def open_file_dialog():
      root = tk.Tk()
      root.withdraw()
      root.attributes('-topmost', True)
      file_path = filedialog.askopenfilename(
          title="Select Excel File",
          filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
      )
      root.destroy()
      return file_path if file_path else None
  ```

---

### 3. Asynchronous / Threading Considerations in Eel
- **Decision**: Execute file dialog calls directly in Eel RPC handler functions.
- **Rationale**: Eel RPC functions run in Python worker threads per WebSocket call, allowing the native OS dialog to block only its call without freezing the Eel WebSocket server.
