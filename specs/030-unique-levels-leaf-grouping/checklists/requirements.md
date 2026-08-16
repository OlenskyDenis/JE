# Requirements Traceability & Checklist (Feature 030)

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Feature Name**: Leaf-First Partitioning & Paragraph Separation in Unique Level View  
**Created**: 2026-08-16  
**Status**: Ready for Planning  

---

## 1. Functional Requirements Traceability Matrix

| Requirement ID | Description | Specification Reference | Target Components |
|---|---|---|---|
| **FR-001** | Categorize unique terms as leaf (`isLeaf: true`) or branch (`isFolder: true`) | [`spec.md`](../spec.md#L94) | `UniqueLevelRenderer.extractUniqueLevels` |
| **FR-002** | Partition level items into sorted `leafItems` and `branchItems` | [`spec.md`](../spec.md#L95) | `UniqueLevelRenderer.extractUniqueLevels` |
| **FR-003** | Render `leafItems` first within each level container | [`spec.md`](../spec.md#L96) | `UniqueLevelRenderer.renderUniqueLevels` |
| **FR-004** | Visual paragraph break / separator when both groups exist | [`spec.md`](../spec.md#L97) | `UniqueLevelRenderer.renderUniqueLevels`, `style.css` |
| **FR-005** | Suppress empty placeholders/dividers on all-leaf or all-branch levels | [`spec.md`](../spec.md#L98) | `UniqueLevelRenderer.renderUniqueLevels` |
| **FR-006** | Dedicated semantic classes (`.level-group-leaves`, `.level-group-branches`) | [`spec.md`](../spec.md#L99) | `style.css`, `unique_level_renderer.js` |
| **FR-007** | Maintain cross-level badges, hover sync, tooltips, and double-click editing | [`spec.md`](../spec.md#L100) | `UniqueLevelRenderer`, `app.js` |
| **FR-008** | Full bilingual dictionary entries (`uk` and `en`) in `i18n.js` | [`spec.md`](../spec.md#L101) | `i18n.js` |
| **FR-009** | Dark theme styling, smooth transitions, and responsive layout | [`spec.md`](../spec.md#L102) | `style.css` |

---

## 2. User Story Coverage

| User Story | Priority | Target Outcome | Status |
|---|---|---|---|
| **US1** | P1 | Leaf items appear first with distinct paragraph separation from branch items | 📝 Specified |
| **US2** | P1 | Feature parity (hover sync, edit modal, cross-match badges) preserved across sub-groups | 📝 Specified |
| **US3** | P2 | Full bilingual localization for Ukrainian and English | 📝 Specified |
