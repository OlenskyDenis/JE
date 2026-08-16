# Data Model: Row-1 Column Metadata & Inferred Data Types

**Feature Branch**: `021-excel-data-types-bug`  
**Spec**: [specs/021-excel-data-types-bug/spec.md](spec.md)  
**Created**: 2026-08-14

---

## 1. Domain Entities & Type Definitions

### 1.1 `VALID_DATA_TYPES`
```python
VALID_DATA_TYPES = (
    "Text",
    "Integer",
    "Decimal",
    "Currency",
    "Percentage",
    "Date",
    "Time",
    "DateTime",
    "Boolean",
)
```

### 1.2 `Row1ColumnMeta` (Internal DTO)
```python
class Row1ColumnMeta:
    name: str           # Cleaned column header string from Row 1
    data_type: str      # Inferred Excel type from VALID_DATA_TYPES
    column_index: int   # 1-based column position in the sheet
    number_format: str  # Raw openpyxl number_format string
```

### 1.3 `HierarchyNode` (Dynamic Composite Node)
```python
class HierarchyNode(HierarchyComponent):
    id: str                         # Unique UUID
    name: str                       # Node name
    children: List[HierarchyNode]   # Nested child components
    parent: Optional[HierarchyNode] # Parent node reference
    data_type: str                  # Canonical Excel data type (Default: "Text")

    @property
    def is_folder(self) -> bool:
        return len(self.children) > 0
```

---

## 2. Eel RPC Serialization Schema

### 2.1 `import_excel_file` Response Payload
```json
{
  "success": true,
  "file_path": "E:/Data/Finance.xlsx",
  "sheets": ["Q1_Sales", "Q2_Sales"],
  "active_sheet": "Q1_Sales",
  "headers": ["Region", "Revenue", "SaleDate"],
  "headers_meta": [
    { "name": "Region", "type": "Text" },
    { "name": "Revenue", "type": "Currency" },
    { "name": "SaleDate", "type": "Date" }
  ],
  "all_headers_meta": {
    "Q1_Sales": [
      { "name": "Region", "type": "Text" },
      { "name": "Revenue", "type": "Currency" },
      { "name": "SaleDate", "type": "Date" }
    ]
  },
  "roots": [
    {
      "id": "node-1",
      "name": "Region",
      "data_type": "Text",
      "is_folder": false,
      "children": []
    },
    {
      "id": "node-2",
      "name": "Revenue",
      "data_type": "Currency",
      "is_folder": false,
      "children": []
    },
    {
      "id": "node-3",
      "name": "SaleDate",
      "data_type": "Date",
      "is_folder": false,
      "children": []
    }
  ]
}
```
