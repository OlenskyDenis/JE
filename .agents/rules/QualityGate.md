---
trigger: always_on
---

# Quality Gate — Pre-Flight & Post-Flight Verification

> **Mandatory Policy:** Every response containing factual claims about the project must pass verification gates. Claims without evidence are fabrications.

## Pre-Flight Gate (Before Responding)

* **Absence Claims Require Proof:** Before stating that any file, component, tool, pattern, skill, or workflow is **absent** from the project — execute a project-wide search (`grep_search` / `list_dir`) and cite the results. A claim of absence without a search artifact is a direct `Honesty.md` violation.
* **Recommendations Require Verification:** Before recommending to **add** something new — search the project to confirm it does not already exist. This applies to rules, skills, files, functions, patterns, and dependencies.
* **Scope-Aware Exploration:** When analyzing the project structure, explore **all** top-level directories — not only the ones already mentioned in conversation. Unknown directories may contain critical context.

## Post-Flight Gate (Before Delivering Final Response)

* **Confidence Audit:** Review every factual claim in the response. Tag unverified claims as `[Hypothesis]` or `[Assumption]`. If a claim cannot be verified — state it explicitly rather than presenting it as fact.
* **Rule Compliance Spot-Check:** For non-trivial responses, verify compliance with at least `ContextFirst.md` and `Honesty.md` before delivering.

## Procedural Enforcement

For complex analysis tasks (architecture reviews, gap analyses, "what's missing" requests), load and follow the `quality-gate` skill which provides detailed verification checklists.
