# Implementation Plan: Full-Stack Use Case Lifecycle Diagrams & Test Verification Checklists (Settings Pilot)

**Branch**: `035-use-case-diagrams-and-test-checklists` | **Date**: 2026-08-17 | **Spec**: [spec.md](spec.md)

**Scope Focus**: Pilot implementation of the hierarchical lifecycle map and verification checklists for the **Settings Sub-System (Налаштування)** in a dedicated directory `specs/035-use-case-diagrams-and-test-checklists/settings/`.

---

## 1. Technical Structure & Artifacts

We structure the Settings pilot into 3 distinct hierarchical levels in `settings/`:

1. **Level A — Atomic Micro-Lifecycles** (`settings/atomic_lifecycles.md`):
   - `ButtonActionLifecycle`: Header Settings button `#btnSettings`, Modal actions `#btnSettingsSave`, `#btnSettingsReset`, `#btnSettingsCancel`.
   - `ModalLifecycle`: `#settingsModal` (Overlay, active/hidden class, focus management, dismiss).
   - `InputControlLifecycle`: `#inputSettingDelimiter` (text input, validation, default fallback).
   - `SelectDropdownLifecycle`: `#selectSettingDefaultType` (options population, type selection).
   - `ToastNotificationLifecycle`: Success/error toast feedback after saving/resetting.

2. **Level B — Macro Full-Stack Lifecycle Sequence** (`settings/macro_lifecycle_diagram.md`):
   - Full-stack parallel sequence between **Frontend** (`SettingsController`, `ModalManager`, `TreeRenderer`, `I18n`) and **Backend** (`eel_bridge.py`, `SettingsService`, `WorkspaceForest`).
   - Sequence covering:
     * Open Modal $\to$ Fetch current settings (`eel.get_settings()`) $\to$ Populate inputs.
     * Edit Delimiter / Default Data Type $\to$ Save (`eel.update_settings(...)`) $\to$ Backend persistence $\to$ Tree leaf path recalculation $\to$ UI refresh.
     * Reset to Defaults (`eel.reset_settings()`) $\to$ Restore standard delimiter (`\`) and `Text` type $\to$ UI refresh.
     * Cancel / Dismiss Modal without saving changes.

3. **Level C — Traceable Verification Checklist** (`settings/verification_checklist.md`):
   - Detailed matrix table mapping each state transition and branch to concrete automated tests in `tests/e2e/test_settings_and_preferences.py`, `tests/unit/test_settings_service.py`, and `tests/e2e/test_automated_interaction_matrix.py`.

---

## 2. Directory Layout

```
specs/035-use-case-diagrams-and-test-checklists/
├── spec.md
├── plan.md
├── quickstart.md
└── settings/
    ├── atomic_lifecycles.md
    ├── macro_lifecycle_diagram.md
    └── verification_checklist.md
```
