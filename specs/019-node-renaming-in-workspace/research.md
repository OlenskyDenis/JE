# Research & Architectural Decisions: In-Place / Modal Node Renaming in Workspace

**Feature**: 019-node-renaming-in-workspace  
**Date**: 2026-08-14  

---

## Decision 1: Modal Edit Flow with Dual Triggers

- **Context**: Node renaming needs to be quick, intuitive, and accessible without cluttering the UI or causing layout jumps.
- **Decision**: Provide two intuitive entry points:
  1. Click on `.btn-node-edit` (Pencil icon ✏️) in `.node-actions`.
  2. Double-click directly on `.node-label`.
  Both open the streamlined `#nodeModal` configured in `'edit'` mode.
- **Rationale**:
  - Reuses existing tested modal CSS and DOM components.
  - Zero layout shifting on the tree canvas.
  - Instant text selection and autofocus allows typing a new name and pressing `Enter` in under 1 second.

---

## Decision 2: Domain-Level Renaming (`HierarchyNode.rename`)

- **Context**: Renaming must enforce data integrity across the composite hierarchy.
- **Decision**: Implement `HierarchyNode.rename(new_name: str)`:
  - Trims leading and trailing whitespace.
  - Rejects empty strings with `ValueError`.
  - Mutates `node.name` in place.
- **Rationale**: Preserves all parent, child, and forest references without re-allocating nodes. All subsequent calls to `PathGenerator.calculate_all_paths` automatically reflect the updated node name.
