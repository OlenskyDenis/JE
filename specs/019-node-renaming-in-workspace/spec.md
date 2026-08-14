# Feature Specification: In-Place / Modal Node Renaming in Workspace

**Feature Branch**: `019-node-renaming-in-workspace`  
**Created**: 2026-08-14  
**Status**: Draft  

**Input**: User directive: "Add a new editing feature for each element in the Hierarchy Constructor Workspace so that the name can be edited"

---

## Constitution Compliance Notice
This specification strictly adheres to the project constitution:
- **Principle I (SDD Scope Enforcement)**: Only specification documentation is authored during this phase. No application source code is modified.
- **Principle II (OOP & Clean State Architecture)**:
  - Clean Domain Encapsulation: `HierarchyNode.name` mutation is managed with validation (whitespace trimming, non-empty validation, delimiter handling).
  - Dynamic Path Cascade: When any parent or child node is renamed, all affected leaf paths automatically update across the tree and in the Export Preview tab.
  - State Integrity: Renaming marks `isDirty = true`, ensuring template auto-synchronization and dirty state interception work seamlessly.
- **Principle IV (Library-First & TDD)**: Unit tests for renaming in domain models (`test_composite.py`) and RPC integration tests (`test_eel_bridge.py`) are specified upfront.
- **Principle VI (System Map First-Load & Proactive Redundancy Audit)**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) consulted.
- **Principle VII (Red Teaming & Zero-Data Stress Testing)**: Validates empty names, leading/trailing whitespace trimming, deep hierarchy path updates, and keyboard shortcuts (`Enter` to submit, `Escape` to cancel).

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Renaming Any Node via Edit Button or Double-Click (Priority: P1) 🎯 MVP

As a user organizing a database or spreadsheet hierarchy, I want to edit and rename any existing node directly in the Hierarchy Constructor Workspace via a modal edit dialog (triggered by clicking the pencil button ✏️ or double-clicking the node label), with autofocused text selection, `Enter` to save, and `Escape` to cancel, so that I can correct typos, refine category names, or adapt structure effortlessly.

**Why this priority**: Core missing CRUD feature in node lifecycle management with zero visual shifting of tree nodes.

**Independent Test**:
1. Create or import a hierarchy tree with node `Finance`.
2. Click the edit pencil button (`.btn-node-edit`) on `Finance` or double-click the label.
3. The edit modal opens pre-filled with `"Finance"`, with the text fully selected and input autofocused.
4. Type `"Accounting & Auditing"` and press `Enter` (or click Save).
5. Verify that the node label in the canvas updates to `"Accounting & Auditing"`.
6. Verify that all child leaf paths update (e.g. `Finance\Q1\Budget` -> `Accounting & Auditing\Q1\Budget`).
7. Verify `isDirty` is set to `true`.

**Acceptance Scenarios**:

1. **Given** any node in the workspace canvas, **When** the user clicks the `.btn-node-edit` pencil action button, **Then** the edit modal appears pre-populated with the current node's name and text selected.
2. **Given** any node in the workspace canvas, **When** the user double-clicks the node label text, **Then** the edit modal appears pre-populated with the current node's name and text selected.
3. **Given** the edit modal, **When** the user enters a new valid name and submits (`Enter` or click Save), **Then** the backend updates the node name, regenerates leaf paths, updates the UI canvas, and marks `isDirty = true`.
4. **Given** the edit modal, **When** the user presses `Escape` or clicks Cancel, **Then** the modal closes without making any changes to the node name.
5. **Given** an attempted rename with an empty string or whitespace only, **When** submitted, **Then** validation rejects the change with an informative toast and retains the existing name.

---

## Edge Cases

- **Renaming Root vs Child**: Renaming a root node or a deeply nested node propagates instantly to all descendant leaf paths without breaking sibling order or parent-child relationships.
- **Special Characters**: Names containing spaces, hyphens, underscores, numbers, or non-Latin Unicode characters (e.g. Cyrillic) must be fully supported.
- **Whitespace Trimming**: Leading and trailing whitespace is automatically stripped before applying the rename.
- **Unchanged Name**: If the user submits without changing the text, no unnecessary dirty state mutation or toast error occurs.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `HierarchyNode` in `src/hierarchy_lib/models/composite.py` MUST support setting a new valid name with automatic whitespace stripping.
- **FR-002**: Backend MUST expose `@eel.expose def rename_node(node_id: str, new_name: str) -> Dict[str, Any]` in `src/app/eel_bridge.py`.
- **FR-003**: `rename_node` MUST reject empty strings or whitespace-only names and return `{ success: False, error: "..." }`.
- **FR-004**: Each node element rendered by `TreeRenderer.renderNode` MUST include a `.btn-node-edit` button (with an SVG pencil icon ✏️) in `.node-actions`.
- **FR-005**: Double-clicking on `.node-label` or clicking `.btn-node-edit` MUST trigger the edit workflow in `src/web/js/app.js`.
- **FR-006**: The edit workflow MUST use the modal with title `"Edit Node Name"`, pre-fill the input with the node's current name, select/focus the input, and bind `Enter` (Submit) and `Escape` (Cancel).
- **FR-007**: Renaming a node MUST update the active tree in `sheet_forests`, recalculate leaf paths in the `Export Preview` tab, and mark `isDirty = true`.
- **FR-008**: Unit tests in `tests/unit/test_composite.py` and integration tests in `tests/integration/test_eel_bridge.py` MUST verify node renaming and leaf path propagation.
- **FR-009**: System map in [`.specify/system_map.md`](../../.specify/system_map.md) MUST be updated to document the `rename_node` RPC endpoint and UI edit controls.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of nodes (roots, folders, leaf nodes) can be renamed in ≤ 2 clicks / keyboard presses.
- **SC-002**: 100% of descendant leaf paths update immediately after a parent node rename.
- **SC-003**: 100% automated test suite pass rate (`python -m pytest`).

---

## Assumptions

- Reuses the existing `#nodeModal` component with dynamic mode switching (`create_root`, `create_child`, `edit_node`) for seamless UI consistency and zero DOM bloat.
