# Data Model & RPC Contracts: Refresh Excel Session

**Feature Branch**: `022-refresh-imported-excel-session`  
**Spec**: [specs/022-refresh-imported-excel-session/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. RPC Contract: `refresh_excel_session()`

### Request
No parameters (uses active session state `current_file_path` and `current_active_sheet` on backend).

### Response: Success
```json
{
  "success": true,
  "file_path": "E:/Data/Finance.xlsx",
  "sheets": ["Sales", "Inventory"],
  "active_sheet": "Sales",
  "headers": ["Region", "Revenue", "SaleDate"],
  "all_headers": {
    "Sales": ["Region", "Revenue", "SaleDate"],
    "Inventory": ["ItemCode", "StockQty"]
  },
  "headers_meta": [
    { "name": "Region", "type": "Text" },
    { "name": "Revenue", "type": "Currency" },
    { "name": "SaleDate", "type": "Date" }
  ],
  "all_headers_meta": {
    "Sales": [
      { "name": "Region", "type": "Text" },
      { "name": "Revenue", "type": "Currency" },
      { "name": "SaleDate", "type": "Date" }
    ],
    "Inventory": [
      { "name": "ItemCode", "type": "Text" },
      { "name": "StockQty", "type": "Integer" }
    ]
  },
  "template_path": null,
  "roots": [
    {
      "id": "uuid-1",
      "name": "Region",
      "data_type": "Text",
      "is_folder": false,
      "children": []
    }
  ]
}
```

### Response: Error
```json
{
  "success": false,
  "error": "Cannot refresh: File 'E:/Data/Finance.xlsx' not found."
}
```
