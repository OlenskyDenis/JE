# Implementation Plan: Relocate 'Add Root Node' Button to Workspace Canvas

**Branch**: `004-relocate-add-root-button` | **Date**: 2026-08-13 | **Spec**: [specs/004-relocate-add-root-button/spec.md](spec.md)

**Input**: Feature specification from `/specs/004-relocate-add-root-button/spec.md`

---

## Summary

Relocate the "Add Root Node" action button (`#btnAddRoot`) from the global `.app-header` toolbar to the top of the "Hierarchy Constructor Workspace" panel (`.tree-panel`). Update HTML structure in `index.html`, enhance panel header and workspace actions in `style.css`, and verify existing JavaScript event listeners in `app.js` continue to function seamlessly without breaking tests or layout.

---

## Technical Context

**Language/Version**: HTML5 + Vanilla CSS + Vanilla JS (Eel Frontend)  
**Primary Dependencies**: None (Standard browser DOM APIs and CSS)  
**Storage**: N/A  
**Testing**: `pytest` (Backend regression) & Browser UI verification  
**Target Platform**: Desktop GUI Web Application via Eel  
**Performance Goals**: Instant modal opening (<50ms), responsive panel header scaling  
**Constraints**: Preserve exact button element ID `#btnAddRoot` for event binding compatibility  

---

## Constitution Check

- **Principle I (SDD Scope Enforcement)**: PASSED. Plan generated before implementation.
- **Principle II (OOP & SOLID)**: PASSED. Presentation layout decoupled cleanly from event controllers.
- **Principle III (GoF Composite Pattern)**: PASSED. Tree structure and composite rendering unchanged.
- **Principle IV (Library-First & TDD)**: PASSED. Preserves frontend-backend contract bindings and existing test coverage.
- **Principle V (Self-Contained Excel & Web UI)**: PASSED. Uses standard Vanilla CSS design tokens.

---

## Project Structure

### Documentation (this feature)

```text
specs/004-relocate-add-root-button/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
└── tasks.md             # Task breakdown & execution tracker
```

### Source Code Files Affected

```text
src/web/
├── index.html           # Move #btnAddRoot from .app-header to .tree-panel header action area
├── css/style.css        # Update .panel-header layout to accommodate panel actions cleanly
└── js/app.js            # Verify event handler binding for #btnAddRoot remains intact
```

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | *Fully compliant with zero architectural complexity additions.* | *N/A* |
