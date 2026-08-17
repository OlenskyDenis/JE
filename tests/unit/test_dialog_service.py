"""Unit tests for FileDialogService using mocked tkinter.filedialog."""

from unittest.mock import MagicMock, patch

from src.hierarchy_lib.services.dialog_service import FileDialogService


@patch("src.hierarchy_lib.services.dialog_service.filedialog.askopenfilename")
@patch("src.hierarchy_lib.services.dialog_service.tk.Tk")
def test_ask_open_file_selected(mock_tk, mock_askopenfilename):
    mock_askopenfilename.return_value = "E:/Data/sample.xlsx"
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    res = FileDialogService.ask_open_file()

    assert res["success"] is True
    assert res["cancelled"] is False
    assert res["file_path"] == "E:/Data/sample.xlsx"
    mock_root.withdraw.assert_called_once()
    mock_root.destroy.assert_called_once()


@patch("src.hierarchy_lib.services.dialog_service.filedialog.askopenfilename")
@patch("src.hierarchy_lib.services.dialog_service.tk.Tk")
def test_ask_open_file_cancelled(mock_tk, mock_askopenfilename):
    mock_askopenfilename.return_value = ""  # empty string on cancel
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    res = FileDialogService.ask_open_file()

    assert res["success"] is True
    assert res["cancelled"] is True
    assert res["file_path"] is None


@patch("src.hierarchy_lib.services.dialog_service.filedialog.asksaveasfilename")
@patch("src.hierarchy_lib.services.dialog_service.tk.Tk")
def test_ask_save_file_selected(mock_tk, mock_asksaveasfilename):
    mock_asksaveasfilename.return_value = "E:/Data/exported.xlsx"
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    res = FileDialogService.ask_save_file(default_name="reorganized.xlsx")

    assert res["success"] is True
    assert res["cancelled"] is False
    assert res["file_path"] == "E:/Data/exported.xlsx"
    mock_root.withdraw.assert_called_once()
    mock_root.destroy.assert_called_once()


@patch("src.hierarchy_lib.services.dialog_service.filedialog.asksaveasfilename")
@patch("src.hierarchy_lib.services.dialog_service.tk.Tk")
def test_ask_save_file_cancelled(mock_tk, mock_asksaveasfilename):
    mock_asksaveasfilename.return_value = ""  # empty string on cancel
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    res = FileDialogService.ask_save_file()

    assert res["success"] is True
    assert res["cancelled"] is True
    assert res["file_path"] is None
