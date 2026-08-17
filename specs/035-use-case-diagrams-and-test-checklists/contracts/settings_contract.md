# Interface & Protocol Contract: Settings Sub-System

**Feature**: 035-use-case-diagrams-and-test-checklists  
**Sub-system**: Settings  
**Date**: 2026-08-17  

---

## 1. Eel RPC Endpoints & Contracts

### `get_settings()`
- **Signature**: `eel.get_settings()() -> Dict[str, Any]`
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

### `update_settings(delimiter, default_data_type)`
- **Signature**: `eel.update_settings(delimiter: Optional[str], default_data_type: Optional[str])() -> Dict[str, Any]`
- **Response**:
  ```json
  {
    "success": true,
    "settings": {
      "delimiter": "/",
      "default_data_type": "Currency"
    },
    "roots": [...]
  }
  ```

### `reset_settings()`
- **Signature**: `eel.reset_settings()() -> Dict[str, Any]`
- **Response**:
  ```json
  {
    "success": true,
    "settings": {
      "delimiter": "\\",
      "default_data_type": "Text"
    },
    "roots": [...]
  }
  ```
