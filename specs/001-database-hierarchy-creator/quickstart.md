# Quickstart Guide: Database Hierarchy Creator

## Environment Prerequisites

- **Python**: 3.12+
- **Package Manager**: `pip` or `uv`
- **Dependencies**: `eel`, `openpyxl`, `pytest`

---

## Developer Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 2. Install Core Dependencies
```bash
pip install eel openpyxl pytest
```

### 3. Run Standalone Core Library Unit Tests (TDD)
Before launching the desktop UI, execute the `pytest` test suite to verify the OOP Composite pattern, path calculation, and Excel parsing logic:
```bash
pytest tests/unit/ -v
```

### 4. Launch Desktop Application
To launch the Eel desktop UI application:
```bash
python -m src.main
```

---

## Directory & Package Layout

- `src/hierarchy_lib/`: Standalone Python library containing Composite OOP models, `PathGenerator`, and `openpyxl` Excel adapters.
- `src/app/`: Eel desktop application entry points and RPC bridge.
- `src/web/`: HTML5, CSS3, and JS frontend files for the drag-and-drop constructor UI.
- `tests/unit/`: Pytest unit tests for core hierarchy models and path calculations.
- `tests/integration/`: Pytest integration tests for Eel bridge endpoints and Excel import/export files.
