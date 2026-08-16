# DTOs & Wire Contracts: Data Transfer Definitions

**Path**: `.specify/system_map/dtos_and_contracts.md`  
**Architectural Layer**: Contract / DTO Layer  
**Protocol**: JSON-RPC over Python Eel WebSocket Bridge

---

## 1. Core Data Transfer Objects (DTOs)

### 1.1 `HierarchyNodeDTO`
Serialized representation of a `HierarchyNode` instance.
```json
{
  "id": "c1f3b890-482a-45c1-968b-59d4c728e5a1",
  "name": "Employees",
  "data_type": "Text",
  "is_folder": false,
  "is_container": false,
  "absolute_path": "Company\\HR\\Employees",
  "children": []
}
```

### 1.2 `WorkspaceForestDTO`
Container payload for multi-root canvas tree rendering.
```json
{
  "roots": [
    {
      "id": "root-uuid-1",
      "name": "Company",
      "data_type": "Text",
      "is_folder": true,
      "is_container": true,
      "absolute_path": "Company",
      "children": [
        {
          "id": "child-uuid-1",
          "name": "Finance",
          "data_type": "Text",
          "is_folder": true,
          "is_container": true,
          "absolute_path": "Company\\Finance",
          "children": [
            {
              "id": "leaf-uuid-1",
              "name": "Revenue",
              "data_type": "Currency",
              "is_folder": false,
              "is_container": false,
              "absolute_path": "Company\\Finance\\Revenue",
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```

### 1.3 `SettingsDTO`
Application configuration payload.
```json
{
  "delimiter": "\\",
  "default_data_type": "Text"
}
```

### 1.4 `ExcelSessionDTO`
Payload returned by `import_excel_file` and `refresh_excel_session`.
```json
{
  "success": true,
  "file_path": "C:\\Users\\User\\Documents\\Data.xlsx",
  "sheets": ["Sales", "Inventory", "HR"],
  "active_sheet": "Sales",
  "headers": ["Region", "Revenue", "OrderDate"],
  "all_headers": {
    "Sales": ["Region", "Revenue", "OrderDate"],
    "Inventory": ["SKU", "Quantity"],
    "HR": ["EmployeeID", "Department"]
  },
  "headers_meta": [
    { "name": "Region", "type": "Text" },
    { "name": "Revenue", "type": "Currency" },
    { "name": "OrderDate", "type": "Date" }
  ],
  "all_headers_meta": {
    "Sales": [
      { "name": "Region", "type": "Text" },
      { "name": "Revenue", "type": "Currency" },
      { "name": "OrderDate", "type": "Date" }
    ],
    "Inventory": [
      { "name": "SKU", "type": "Text" },
      { "name": "Quantity", "type": "Integer" }
    ],
    "HR": [
      { "name": "EmployeeID", "type": "Integer" },
      { "name": "Department", "type": "Text" }
    ]
  },
  "template_path": null,
  "roots": [ /* HierarchyNodeDTO objects */ ]
}
```

### 1.5 `RejectionDTO`
Payload returned when a cycle or invalid move is rejected.
```json
{
  "success": false,
  "rejection_reason": "Cannot move parent node 'Company' into its own descendant 'Revenue'.",
  "roots": [ /* Current unmodified tree roots */ ]
}
```

---

## 2. Standard RPC Response Wrapper Contract

All RPC bridge endpoints return an object matching the following structure:
```json
{
  "success": true,
  "error": null,
  /* Additional method-specific payload fields */
}
```
If an operation fails:
```json
{
  "success": false,
  "error": "Human-readable localized or exception error message."
}
```
