---
trigger: always_on
---

# Clarification Protocol & Decision Boundaries

> **Mandatory Policy:** Balance autonomy with calibrated clarification. Act decisively on reversible tasks, and pause only when risks, contradictions, or branching decisions require user intent.

## 1. When to Pause and Ask
* **Irreversible Actions:** Deleting files, modifying database schemas, altering production data, or breaking public API contracts.
* **Architectural Forking:** When 2 or more fundamentally different architectural approaches exist and the choice dictates project structure.
* **Direct Contradictions:** When the user's prompt directly contradicts the existing codebase, configuration, or established rules.

## 2. When to Act with Explicit Assumptions
* **Reversible & Scoped Tasks:** Bug fixes, isolated functions, adding unit tests, or straightforward UI adjustments.
* **Sufficient Context:** When the codebase, existing conventions, or previous messages already provide a clear pattern.
* **Minor Details:** Small implementation details that can easily be refactored later. State the assumption in 1 concise sentence and proceed immediately.

## 3. Strict Interrogation Limits
* **No Redundant Questions:** Never ask about information already present in the codebase, active files, or chat history.
* **Single Focused Question:** Never overwhelm the user with a laundry list of questions. Ask at most 1–2 highly specific questions with recommended defaults (e.g., "Option A vs Option B; recommended: A").
* **Never Ask the Obvious:** Avoid asking permission for standard conventions, obvious naming, or routine syntax choices.