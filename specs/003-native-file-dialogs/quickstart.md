# Quickstart & End-to-End Validation Guide: Native File Dialogs

**Feature**: `003-native-file-dialogs`  
**Date**: 2026-08-13  
**Status**: Complete  

---

## Prerequisites

- **Python**: Python 3.10+ with standard `tkinter` package.
- **Dependencies**: `eel`, `openpyxl`, `pytest` installed.

---

## Automated Verification

Run unit tests for file dialog service and Eel RPC endpoints:

```bash
python -m pytest tests/unit/test_dialog_service.py -v
python -m pytest tests/integration/test_eel_bridge.py -v
```

---

## Manual End-to-End UI Verification

1. **Launch Desktop App**:
   ```bash
   python -m src.app.main
   ```
2. **Test Excel Import Dialog**:
   - Click **Import Excel** button.
   - Confirm a native OS open file picker window opens directly in front of the application window.
   - Verify file extension filter defaults to Excel files (`*.xlsx`).
   - Select a valid `.xlsx` file and click Open.
   - Confirm the dialog closes and sheet headers are loaded into the sidebar catalog.
3. **Test Cancel Import Dialog**:
   - Click **Import Excel** button again.
   - Click **Cancel** in the OS file picker.
   - Confirm the dialog closes with zero error messages and the current workspace remains untouched.
4. **Test Excel Export Dialog**:
   - Add nodes to the tree builder.
   - Click **Export Excel** button.
   - Confirm a native OS save file dialog opens pre-filled with default filename `reorganized_headers_export.xlsx`.
   - Choose a target folder, enter a filename, and click Save.
   - Confirm the file is created at the chosen path and contains horizontal Row 1 leaf paths.
