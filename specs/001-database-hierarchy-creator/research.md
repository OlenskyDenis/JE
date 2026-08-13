# Phase 0 Research & Technology Decisions: Database Hierarchy Creator

## Technical Decisions Summary

| Component | Choice / Recommendation | Rationale & Alternatives Evaluated |
|---|---|---|
| **Python Version** | Python 3.12 | Modern type hinting, high performance, native support for dataclasses and abstract base classes (ABC). |
| **Desktop Application Wrapper** | `Eel` | Lightweight HTML/JS/CSS desktop wrapper using Chrome/Chromium app mode via websockets. Avoids heavy Electron dependencies while enabling rich browser drag-and-drop web UX. |
| **Excel Processing Library** | `openpyxl` | Native OpenXML `.xlsx` reader/writer written in pure Python. Runs in 100% self-contained environments without MS Excel application or COM interop. |
| **Hierarchy Modeling** | Gang of Four (GoF) Composite Design Pattern | Object-Oriented design separating leaf items (`LeafNode`) from containers (`CompositeNode`) under a common base abstraction (`HierarchyComponent`). |
| **Core Architecture** | Standalone Python Library (`hierarchy_lib`) | Decouples business logic, path calculation, and Excel parsing into an isolated library (`src/hierarchy_lib`). UI acts solely as a consumer. |
| **Testing Framework** | `pytest` | Standard Python testing framework for running unit tests on core hierarchy models, path generators, and Excel adapters. |
| **Frontend Stack** | HTML5, Vanilla CSS3, Vanilla JS (ES6+) | Maximum control over drag-and-drop hit testing (3-zone calculation: top/bottom 25% for sibling reordering, center 50% for child nesting) without heavy frontend framework overhead. |

---

## Technical Details & Feasibility Studies

### 1. Eel Bridge Protocol Architecture
- **Websocket Communication**: Eel exposes Python functions decorated with `@eel.expose` to JS (e.g., `eel.import_excel_file(file_path)`), and calls JS functions from Python (e.g., `eel.render_tree(tree_json)`).
- **Decoupling**: The Eel interface layer (`src/app/eel_bridge.py`) converts web JSON payloads into `hierarchy_lib` domain objects (`HierarchyComponent`), preventing UI dependencies in core library code.

### 2. Standalone Core Library (`hierarchy_lib`)
- **Hierarchy Component Interface (`HierarchyComponent`)**: Abstract base class defining `id`, `name`, `parent`, `get_absolute_path()`, and traversal protocol.
- **CompositeNode**: Holds a list of `HierarchyComponent` children. Handles `add_child()`, `remove_child()`, `move_child()`, cycle detection validation, and recursive path calculation.
- **LeafNode**: Terminal node in hierarchy representing data items.
- **PathGenerator**: Traverser that walks parent references up to root, joining names with backslashes (`\`) for multi-root trees.

### 3. Excel Processing Specification (`openpyxl`)
- **Import Adapter (`openpyxl`)**:
  1. Opens uploaded `.xlsx` workbook using `openpyxl.load_workbook(filename, read_only=True)`.
  2. Iterates through each sheet.
  3. Reads Row 1 / Cell A1 text content.
  4. Splits the text string on backslashes (`\`) into path segments.
  5. Dynamically builds or updates the in-memory Composite node tree.
- **Export Adapter (`openpyxl`)**:
  1. Creates a new workbook via `openpyxl.Workbook()`.
  2. Iterates through all leaf node paths in the Composite forest.
  3. Writes each path segment into sequential rows (Column A, Row 1 = Segment 1, Row 2 = Segment 2, etc.) with one element per cell per row.
  4. Saves `.xlsx` file to user-specified output path.

### 4. Drag-and-Drop Hit-Testing Algorithm (Frontend UI)
- **Three-Zone Target Detection**:
  - `targetRect = element.getBoundingClientRect()`
  - `relativeY = (mouseY - targetRect.top) / targetRect.height`
  - `if relativeY < 0.25`: Action = `BEFORE_SIBLING`
  - `else if relativeY > 0.75`: Action = `AFTER_SIBLING`
  - `else`: Action = `NEST_CHILD`
- **Cycle Prevention**: Prior to drop execution, JS queries the backend or checks local tree model. If `targetNode` is an ancestor of `draggedNode` or equal to `draggedNode`, the drop is rejected, cursor displays `not-allowed`, and on drop release, the element snaps back with a warning toast notification.
