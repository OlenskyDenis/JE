# Data Model & Schema: Lifecycle Entities & Verification Checklists

**Feature**: 035-use-case-diagrams-and-test-checklists  
**Date**: 2026-08-17  

---

## 1. Schema for Lifecycle Diagram Entities

```json
{
  "entity_name": "string (e.g. Settings, MultiSheetSession, ViewModes)",
  "micro_lifecycles": [
    {
      "component": "string (e.g. ButtonActionLifecycle)",
      "target_selectors": ["string"],
      "states": ["Idle", "Hovered", "ActivePressed", "Processing", "Disabled"]
    }
  ],
  "macro_sequence": {
    "participants": ["User", "DOM", "FrontendController", "EelRPC", "BackendService", "DomainModel"],
    "phases": [
      {
        "phase_name": "string",
        "user_trigger": "string",
        "frontend_actions": ["string"],
        "rpc_calls": ["string"],
        "backend_mutations": ["string"],
        "visual_feedback": ["string"]
      }
    ]
  }
}
```

---

## 2. Schema for Verification Checklist Items

```json
{
  "checklist_item_id": "string (e.g. CHK-SET-01)",
  "subsystem": "string",
  "phase_reference": "string",
  "pre_condition": "string",
  "action_trigger": "string",
  "expected_frontend_state": {
    "selectors": ["string"],
    "visibility": "boolean",
    "classes": ["string"],
    "values": ["string"]
  },
  "expected_backend_state": {
    "rpc_method": "string",
    "returned_data": "dict",
    "service_state": "dict"
  },
  "mapped_test_path": "string (e.g. tests/e2e/test_settings_and_preferences.py::test_name)",
  "status": "PASS | FAIL"
}
```
