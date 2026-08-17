---
name: spec-workflow
description: >
  Standardized feature lifecycle and specification workflow for the JE project.
  Use when planning, creating, breaking down, implementing, or validating features under specs/NNN-feature-name/.
---

# JE Feature Specification & Lifecycle Workflow

> **Purpose:** Standard procedure for taking a feature from initial idea through specification, testing, implementation, and commit.

---

## 1. Feature Lifecycle Overview

Every non-trivial feature in JE follows the 5-phase lifecycle:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. RESEARCH │ ──► │   2. SPEC    │ ──► │   3. PLAN    │ ──► │  4. EXECUTE  │ ──► │  5. VERIFY   │
│   & DISCOVERY│     │ (spec.md)    │     │(plan/tasks)  │     │    & TDD     │     │ (E2E/Quality)│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 2. Directory Structure (`specs/NNN-feature-name/`)

The next spec number is the highest current number in `specs/` incremented by 1 (formatted as 3-digit zero-padded, e.g. `032-new-feature`).

```
specs/NNN-feature-name/
├── spec.md           # Requirements, user stories, edge cases (Ukrainian)
├── plan.md           # Technical architecture, layers, components affected
├── tasks.md          # Ordered checklist with progress tags [ ] / [x]
├── quickstart.md     # (Optional) Quick run/verification commands
└── data-model.md     # (Optional) Data structure or DTO schema changes
```

---

## 3. Git Branching & Commit Conventions

* **Branch Creation:** `git checkout -b NNN-feature-name` (from latest `main`).
* **Commit Message Format:**
  * Spec features: `NNN-spec-name: Short imperative summary in English`
  * Example: `032-export-json: Add JSON hierarchy exporter and test suite`
* **Rule Reference:** Always comply with [`Git.md`](file:///e:/JE/.agents/rules/Git.md).

---

## 4. Phase Details & Checklists

### Phase 1: Research & Discovery
- [ ] Inspect existing layers (`models/`, `services/`, `adapters/`, `web/js/`).
- [ ] Verify no duplicate logic will be introduced (consult [`DRY.md`](file:///e:/JE/.agents/rules/DRY.md) and [`hierarchy-domain`](file:///e:/JE/.agents/skills/hierarchy-domain/SKILL.md)).

### Phase 2: Spec Authoring (`spec.md`)
- [ ] Create `specs/NNN-feature-name/spec.md`.
- [ ] Detail user scenarios, UI/RPC interactions, and edge cases in Ukrainian.

### Phase 3: Plan & Tasks Breakdown (`plan.md` & `tasks.md`)
- [ ] Write `plan.md` defining backend models/services and frontend singletons affected.
- [ ] Create `tasks.md` with granular, atomic steps organized by phases.

### Phase 4: Implementation (TDD & Quality Gates)
- [ ] Write failing unit/integration tests first in `tests/unit/` or `tests/integration/`.
- [ ] Implement domain logic adhering to [`SOLID.md`](file:///e:/JE/.agents/rules/SOLID.md) and [`KISS.md`](file:///e:/JE/.agents/rules/KISS.md).
- [ ] Expose Eel bridge methods with `@eel.expose` and proper `try/except` dictionary contracts.
- [ ] Update frontend singleton (`App`, renderers, `i18n.js` with UK + EN translations).

### Phase 5: Verification & Delivery
- [ ] Run full unit & integration tests: `python -m pytest tests/unit tests/integration`
- [ ] Run relevant Playwright E2E tests: `python -m pytest tests/e2e/`
- [ ] Perform post-flight quality check ([`QualityGate.md`](file:///e:/JE/.agents/rules/QualityGate.md)).
- [ ] Commit changes according to [`Git.md`](file:///e:/JE/.agents/rules/Git.md).
