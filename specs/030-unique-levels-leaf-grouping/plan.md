# Implementation Plan: Leaf-First Partitioning & Ergonomic Visual Separation in Unique Level View

**Feature Branch**: `030-unique-levels-leaf-grouping`  
**Created**: 2026-08-16  
**Status**: Completed  
**Spec**: [specs/030-unique-levels-leaf-grouping/spec.md](spec.md)  
**Data Model**: [specs/030-unique-levels-leaf-grouping/data-model.md](data-model.md)  
**Checklist**: [specs/030-unique-levels-leaf-grouping/checklists/requirements.md](checklists/requirements.md)  

---

## 1. Architecture & Design Overview

This feature refactors the level row rendering engine and styling in `UniqueLevelRenderer` (`src/web/js/unique_level_renderer.js`) and `src/web/css/style.css` to:
1. **Partition items leaf-first**: Leaf elements (`isLeaf === true`) appear first, followed by an understated paragraph divider, followed by branch elements (`isFolder === true`).
2. **Visual Ergonomics & Color Harmony**:
   - Align surface colors with `Excel Blocks` and `Tree View` using `--bg-panel` (`#1e293b`).
   - Clean, lightweight chips with subtle borders (`#0f172a` / `#131d2e` and `1px solid rgba(255, 255, 255, 0.08)`).
   - Removed harsh saturated left borders on chips to eliminate visual noise and eye strain.
   - Subtle, minimalist sub-group titles and soft neutral/sky pill tags.
   - Understated `1px` paragraph separator line.

All existing features (cross-level match highlighting, hover sync, frequency badges, tooltips, and double-click batch editing) are preserved with 100% fidelity.

---

## 2. Implementation Phases

### Phase 1: Baseline Test Verification
- Run test suite (`python -m pytest`) to verify existing tests pass with zero errors.

### Phase 2: Core Level Deduplication & Partitioning (`src/web/js/unique_level_renderer.js`)
- Update `extractUniqueLevels(roots)` to partition into `leafItems` and `branchItems` sorted alphabetically.
- Update `renderUniqueLevels(roots, containerEl)` to render leaf group first, visual paragraph separator when both exist, and branch group second.

### Phase 3: Localization & Internationalization (`src/web/js/i18n.js`)
- Register Ukrainian (`uk`) and English (`en`) dictionary keys for sub-group titles and badges.

### Phase 4: Ergonomic CSS Dark Theme Styling (`src/web/css/style.css`)
- Implement relaxed, eye-friendly styles for `.level-row-container`, `.level-subgroup`, `.level-group-separator`, and `.level-header-chip` matching Excel Blocks and Tree View.

### Phase 5: Verification & Contract Tests
- Add contract test to `tests/unit/test_frontend_contracts.py`.
- Run full pytest test suite (78 passing tests).
