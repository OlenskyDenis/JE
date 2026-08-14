# Technical Research: Row-1 Excel Column Format Mapping & Streaming Architecture

**Feature Branch**: `021-excel-data-types-bug`  
**Spec**: [specs/021-excel-data-types-bug/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Research Question: How does openpyxl store and expose column-level formatting?

### Context & Decision
When users format a column in Excel (e.g. by selecting Column B and setting format to `Date` or `Currency`), Excel writes formatting descriptors into two locations in the XML package:
1. **Cell-Level Format (`cell.number_format`)**: Stored on the cell XML (`<c s="X" ...>`).
2. **Column-Level Format (`ws.column_dimensions[col_letter].number_format`)**: Stored on the `<col min="2" max="2" style="X" ...>` element.
3. **Cell Data Type Flag (`cell.data_type`)**: Stored on cell attributes (e.g. `s` for string, `b` for boolean, `d` for date, `n` for numeric, `e` for error).

### Decision
`ExcelHierarchyAdapter.read_row1_headers_and_types()` checks `cell.number_format`, `column_dimensions[col_letter].number_format`, and `cell.data_type` in a single pass across Row 1 (`max_row=1`).

---

## 2. Standard Excel Number Format Pattern Matching Engine

### Mapping Table

| Detected Format Pattern in Excel | Classification Logic | Target `data_type` |
|---|---|---|
| Contains `yy`, `yyyy`, `dd`, `d-mmm`, `dd.mm`, `m/d/yy`, date format IDs (14, 15, 16, 17, 22) without time | `has_date and not has_time` | **`Date`** |
| Contains `hh`, `ss`, `am/pm`, `h:mm`, time format IDs (18, 19, 20, 21) without date | `has_time and not has_date` | **`Time`** |
| Contains both date (`yy`, `dd`) and time (`hh`, `ss`, `am/pm`) | `has_date and has_time` | **`DateTime`** |
| Contains `$`, `€`, `£`, `грн`, `₽`, `¥`, `руб`, `¤`, or currency format IDs (5, 6, 7, 8, 41, 42, 43, 44) | Currency symbol / format ID | **`Currency`** |
| Contains `%` or percentage format IDs (9, 10) | `has_percentage` | **`Percentage`** |
| Contains `0.00`, `0.000`, `0.0000`, `#.00`, or decimal format IDs (2, 4) | `is_decimal` | **`Decimal`** |
| Contains `0`, `#,##0`, `0_`, or integer format IDs (1, 3) | `is_integer` | **`Integer`** |
| `cell.data_type == 'b'` or boolean naming/format | `is_boolean` | **`Boolean`** |
| `@`, `General`, empty, None, or unrecognized text format | Fallback | **`Text`** |

---

## 3. Performance & Memory Impact Analysis

- **Streaming Constraint**: `max_row=1` strictly guarantees that reading an Excel file with 1,000,000 rows executes in $O(1)$ time and memory.
- **Single Pass vs Dual Pass**: Consolidating header reading and format inspection into `read_row1_headers_and_types()` cuts workbook opening and sheet parsing time in half compared to separate calls.
