# Domain Data Model: Optimized Streaming Excel Adapter

**Feature**: 007-excel-import-optimization  
**Date**: 2026-08-14  

## Component Architecture

```
+-------------------------------------------------------------+
|                   ExcelHierarchyAdapter                     |
+-------------------------------------------------------------+
| + get_sheet_names(file_path_or_stream) -> List[str]         |
| + read_row1_headers(file_path_or_stream, sheet_name,        |
|                     max_empty_consecutive: int = 10)        |
|                     -> List[str]                            |
| + export_horizontal_row1_leaf_paths(...) -> int             |
+-------------------------------------------------------------+
                              |
                              v (streams via)
+-------------------------------------------------------------+
|            openpyxl.load_workbook(read_only=True)           |
|  - sheet.iter_rows(max_row=1, values_only=True)             |
+-------------------------------------------------------------+
                              |
                              v (processes via)
+-------------------------------------------------------------+
|                       HeaderService                         |
| + process_headers(raw_headers) -> List[str]                 |
+-------------------------------------------------------------+
```

### Parameters and Constants

| Entity / Param | Type | Default | Description |
|---|---|---|---|
| `read_only` | `bool` | `True` | Instructs openpyxl to use XML streaming pull parser |
| `max_row` | `int` | `1` | Restricts streaming to the first row only |
| `values_only` | `bool` | `True` | Directly streams raw cell values without creating `Cell` objects |
| `max_empty_consecutive` | `int` | `10` | Safety cutoff limit for stopping row scanning upon empty cells |
