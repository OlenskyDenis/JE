# Quality & Requirements Checklist: Feature 020 Leaf Element Data Types

**Feature Branch**: `020-leaf-element-data-types`  
**Date**: 2026-08-14  

---

## Constitution & Architecture Compliance

- [ ] **Principle I (SDD Scope Enforcement)**: Spec and Plan completed before implementation. No source code touched in specify/plan phases.
- [ ] **Principle II (OOP & Clean State)**: `HierarchyNode` encapsulates `data_type` and validation; services remain modular and single-responsibility.
- [ ] **Principle III (GoF Dynamic Composite)**: Leaf and folder transitions are dynamic (`len(children) == 0`).
- [ ] **Principle IV (Library-First & TDD)**: Unit tests for domain models, adapters, and RPC bridge written and passing.
- [ ] **Principle V (Self-Contained Excel)**: openpyxl streaming and workbook creation used with zero COM/MS Excel installation requirements.
- [ ] **Principle VI (System Map Sync)**: [`.specify/system_map.md`](../../.specify/system_map.md) updated with all new components, endpoints, and UI elements.
- [ ] **Principle VII (Red Teaming & Zero-Data)**: Tested clean-slate creation, child deletion conversion, empty sheets, and format fallbacks.

---

## Functional Requirements Verification

- [ ] **FR-001**: `HierarchyNode` holds `data_type: Optional[str] = "Text"`.
- [ ] **FR-002**: `to_dict()` outputs `"data_type": self.data_type`.
- [ ] **FR-003**: `set_data_type(data_type: str)` validates against standard Excel types.
- [ ] **FR-004**: 9 standard Excel types supported (`Text`, `Integer`, `Decimal`, `Currency`, `Percentage`, `Date`, `Time`, `DateTime`, `Boolean`).
- [ ] **FR-005**: `ExcelHierarchyAdapter` infers column types from cell data and number formats on sample rows (Rows 2..100).
- [ ] **FR-006**: `import_excel_file` returns header metadata with detected data types.
- [ ] **FR-007**: Dragging from Header Catalog sidebar inherits the detected `data_type`.
- [ ] **FR-008**: Removing all children of a folder dynamically transforms it into a typed leaf.
- [ ] **FR-009**: `export_multi_sheet_template` applies openpyxl `number_format` strings to exported columns.
- [ ] **FR-010**: `update_node` / `update_node_type` RPC endpoints exposed and tested.
- [ ] **FR-011**: `.node-type-badge` rendered on leaf nodes in canvas and in `Export Preview`.
- [ ] **FR-012**: `#selectNodeType` integrated into `#nodeModal`.
- [ ] **FR-013**: Modal dynamically shows/hides type selector based on folder vs leaf state.
- [ ] **FR-014**: System map updated and verified.
- [ ] **FR-015**: 100% automated test suite pass rate.
