"""ExcelHierarchyAdapter facade delegating to ExcelReader and ExcelWriter."""

from typing import Any, BinaryIO, Dict, List, Optional, Tuple, Union

from src.hierarchy_lib.adapters.excel_reader import ExcelReader
from src.hierarchy_lib.adapters.excel_writer import ExcelWriter


class ExcelHierarchyAdapter:
    """Facade adapter for importing and exporting Composite hierarchy trees to/from Excel (.xlsx) files."""

    EXCEL_TYPE_FORMAT_MAP = ExcelWriter.EXCEL_TYPE_FORMAT_MAP

    @staticmethod
    def get_sheet_names(file_path_or_stream: Union[str, BinaryIO]) -> List[str]:
        """Returns the list of worksheet names available in the workbook."""
        return ExcelReader.get_sheet_names(file_path_or_stream)

    @staticmethod
    def _map_format_to_data_type(
        number_format: Optional[str],
        data_type_flag: Optional[str] = None,
        header_name: Optional[str] = None,
        default_data_type: Optional[str] = None,
    ) -> str:
        """Maps Excel number format string and cell data_type flag to one of standard Excel types."""
        return ExcelReader.map_format_to_data_type(
            number_format=number_format,
            data_type_flag=data_type_flag,
            header_name=header_name,
            default_data_type=default_data_type,
        )

    @staticmethod
    def read_row1_headers_and_types(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        max_empty_consecutive: int = 10,
        default_data_type: Optional[str] = None,
    ) -> List[Tuple[str, str]]:
        """Reads Row 1 cells and detects column data types."""
        return ExcelReader.read_row1_headers_and_types(
            file_path_or_stream=file_path_or_stream,
            sheet_name=sheet_name,
            max_empty_consecutive=max_empty_consecutive,
            default_data_type=default_data_type,
        )

    @staticmethod
    def read_row1_headers(
        file_path_or_stream: Union[str, BinaryIO],
        sheet_name: str,
        max_empty_consecutive: int = 10,
        default_data_type: Optional[str] = None,
    ) -> List[str]:
        """Reads clean, deduplicated, sorted Row 1 headers from the specified sheet."""
        return ExcelReader.read_row1_headers(
            file_path_or_stream=file_path_or_stream,
            sheet_name=sheet_name,
            max_empty_consecutive=max_empty_consecutive,
            default_data_type=default_data_type,
        )

    @staticmethod
    def export_multi_sheet_template(
        file_path_or_stream: Union[str, BinaryIO, None],
        sheet_leaf_paths_map: Dict[str, Any],
        output_path: str,
    ) -> int:
        """Constructs an openpyxl.Workbook with Row 1 headers and data type formats."""
        return ExcelWriter.export_multi_sheet_template(
            file_path_or_stream=file_path_or_stream,
            sheet_leaf_paths_map=sheet_leaf_paths_map,
            output_path=output_path,
        )
