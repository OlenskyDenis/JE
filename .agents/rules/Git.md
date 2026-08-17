

# Git Workflow & Commit Conventions

> **Mandatory Policy:** Follow the established branching and commit conventions to maintain a clean, navigable project history.

## Branching Strategy

* **Main branch:** `main` — stable, deployable state.
* **Feature branches:** Named by spec number: `NNN-short-description` (e.g., `031-playwright-e2e-testing`). For features without a spec: `feature/short-description`.
* **Current branch:** Always check before committing. Never commit directly to `main` during active feature work.

## Commit Message Format

* **Spec-linked features:** `NNN-spec-name: Brief Description` (e.g., `031-playwright-e2e-testing: Full Project Playwright E2E Automated Testing Suite`).
* **Conventional commits (non-spec):** `type(scope): description` — types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`.
* **Language:** English.
* **Imperative mood** is preferred but not strictly enforced (both "Add feature" and "Added feature" appear in history).

## Workflow

* One commit per logical change. Avoid mega-commits mixing unrelated changes.
* Specs live in `specs/NNN-feature-name/` and are committed alongside (or before) implementation.
