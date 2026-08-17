"""FileDialogService wrapping Python standard library tkinter.filedialog."""

import tkinter as tk
from tkinter import filedialog
from typing import Any, Dict, List, Optional, Tuple


class FileDialogService:
    """Service wrapping native desktop OS open and save file dialogs."""

    @staticmethod
    def _create_hidden_root() -> tk.Tk:
        """Creates a hidden, topmost Tk root window to suppress background window popups."""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        try:
            root.focus_force()
        except Exception:
            pass
        return root

    @classmethod
    def ask_open_file(
        cls, title: str = "Select Excel File", filetypes: Optional[List[Tuple[str, str]]] = None
    ) -> Dict[str, Any]:
        """Opens a native OS open file dialog for selecting an Excel file."""
        if filetypes is None:
            filetypes = [("Excel Files", "*.xlsx"), ("All Files", "*.*")]

        root = None
        try:
            root = cls._create_hidden_root()
            path = filedialog.askopenfilename(parent=root, title=title, filetypes=filetypes)
            file_path = str(path).strip() if path else None
            return {"success": True, "cancelled": not bool(file_path), "file_path": file_path, "error": None}
        except Exception as e:
            return {"success": False, "cancelled": True, "file_path": None, "error": str(e)}
        finally:
            if root is not None:
                try:
                    root.destroy()
                except Exception:
                    pass

    @classmethod
    def ask_save_file(
        cls,
        title: str = "Save Reorganized Excel File",
        default_name: str = "reorganized_headers_export.xlsx",
        defaultextension: str = ".xlsx",
        filetypes: Optional[List[Tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Opens a native OS save file dialog for choosing destination path."""
        if filetypes is None:
            filetypes = [("Excel Files", "*.xlsx"), ("All Files", "*.*")]

        root = None
        try:
            root = cls._create_hidden_root()
            path = filedialog.asksaveasfilename(
                parent=root,
                title=title,
                initialfile=default_name,
                defaultextension=defaultextension,
                filetypes=filetypes,
            )
            file_path = str(path).strip() if path else None
            return {"success": True, "cancelled": not bool(file_path), "file_path": file_path, "error": None}
        except Exception as e:
            return {"success": False, "cancelled": True, "file_path": None, "error": str(e)}
        finally:
            if root is not None:
                try:
                    root.destroy()
                except Exception:
                    pass
