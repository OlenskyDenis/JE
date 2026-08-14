# Quickstart & Verification Guide: Excel Import Performance Optimization

**Feature**: 007-excel-import-optimization  
**Date**: 2026-08-14  

## 1. Automated Test Execution

Run the complete test suite to verify streaming mode and cutoff tests:

```powershell
python -m pytest tests/unit/test_excel_adapter.py
python -m pytest
```

## 2. Test Cases Covered

1. **Large Sheet Performance**:
   - Create a workbook with 10,000+ data rows in Rows 2–10,000.
   - Verify `read_row1_headers` executes in <50ms without loading lower rows.
2. **10 Consecutive Empty Cell Safety Cutoff**:
   - Create a sheet with headers in columns 1–3, 10 empty columns (4–13), and a trailing column 14.
   - Verify scanning stops at column 13 and returns only headers from columns 1–3.
3. **Small Gaps (< 10 cells) Supported**:
   - Create a sheet with headers in column 1, empty columns 2–4 (3 empty cells), and column 5 with header.
   - Verify scanning continues across the 3-cell gap and returns both headers.
4. **Read-Only Workbook Closure**:
   - Verify no open file handle leaks or locked files after reading.
