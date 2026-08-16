# Data Model & Contracts: Settings Configuration

**Feature Branch**: `026-settings-menu-config`  
**Spec**: [specs/026-settings-menu-config/spec.md](spec.md)  
**Date**: 2026-08-16

---

## 1. Data Schema

### `AppSettings` (Data Transfer Object / Dictionary)
```typescript
interface AppSettings {
    delimiter: string;          // 1 to 3 characters, default: "\\"
    default_data_type: string;  // One of standard Excel types, default: "Text"
}
```

### Supported Standard Data Types
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

---

## 2. Configuration Storage Schema (`settings.json`)

```json
{
  "delimiter": "\\",
  "default_data_type": "Text"
}
```

---

## 3. Eel RPC API Contracts

### 3.1 `get_settings()`
- **Parameters**: None
- **Response**:
  ```json
  {
    "success": true,
    "settings": {
      "delimiter": "\\",
      "default_data_type": "Text"
    }
  }
  ```

### 3.2 `update_settings(delimiter: str, default_data_type: str)`
- **Parameters**:
  - `delimiter`: String, stripped, length 1..3
  - `default_data_type`: String matching one of `VALID_DATA_TYPES`
- **Response (Success)**:
  ```json
  {
    "success": true,
    "settings": {
      "delimiter": "/",
      "default_data_type": "Decimal"
    },
    "roots": [ /* Updated active tree roots with recalculated absolute_path */ ]
  }
  ```
- **Response (Validation Error)**:
  ```json
  {
    "success": false,
    "error": "Invalid delimiter or unsupported data type."
  }
  ```

---

## 4. Frontend LocalStorage Contract

- **Storage Key**: `je_settings_config`
- **Stored Value (JSON string)**:
  ```json
  {
    "delimiter": "\\",
    "default_data_type": "Text"
  }
  ```
