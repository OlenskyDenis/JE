---
name: quality-gate
description: >
  Procedural verification checklists for pre-flight and post-flight quality gates.
  Use when performing project analysis, gap assessments, architecture reviews,
  or any task where factual claims about the project are made.
---

# Quality Gate — Verification Checklists

> **Purpose:** Concrete, step-by-step verification procedures that convert abstract rules into auditable actions. Each checklist item requires a tool call — not a mental check.

---

## Pre-Flight Checklist (Run BEFORE Formulating Conclusions)

### 1. Project Exploration Gate

Before answering questions about "what exists" or "what's missing":

- [ ] **List project root** — `list_dir` on the workspace root to discover ALL top-level directories.
- [ ] **Explore unknown directories** — Any directory not yet examined must be listed before claiming its contents are known.
- [ ] **Search before claiming absence** — For every component/tool/pattern you intend to say is "missing" or "absent", execute `grep_search` with relevant keywords across the entire project. Record the search and its result.

### 2. Claim Verification Gate

For every factual statement about the project:

| Claim Type | Required Verification | Tool |
|---|---|---|
| "File X doesn't exist" | `grep_search` for filename + `list_dir` on likely directories | `grep_search`, `list_dir` |
| "Pattern Y is not used" | `grep_search` for pattern keywords project-wide | `grep_search` |
| "Tool/Skill Z is absent" | `list_dir` on `.agents/skills/`, `.github/skills/`, `.specify/` | `list_dir` |
| "No convention for W" | `grep_search` for convention keywords in rules, constitution, configs | `grep_search` |

### 3. Context Completeness Gate

Before proposing architectural recommendations:

- [ ] **Constitution read?** — Verify `.specify/memory/constitution.md` has been loaded and its principles cross-referenced.
- [ ] **System map consulted?** — Verify `.specify/system_map.md` has been loaded for architecture context.
- [ ] **Existing skills inventoried?** — Check both `.agents/skills/` AND `.github/skills/` for existing capabilities.
- [ ] **Speckit workflow checked?** — Check `.specify/workflows/`, `.specify/templates/`, `.specify/integrations/` for existing SDD infrastructure.

---

## Post-Flight Checklist (Run BEFORE Delivering Response)

### 4. Confidence Audit

Review every factual claim in the response:

- [ ] **Verified claims** — Backed by tool output (grep result, file content, directory listing). Present as fact.
- [ ] **Unverified claims** — No tool output backing them. Tag explicitly as `[Hypothesis]` or `[Assumption]`.
- [ ] **Absence claims** — Every "X is missing/absent" has a corresponding search that returned 0 results. If no search was run → either run it now or retract the claim.

### 5. Rule Compliance Spot-Check

| Rule | Quick Check |
|---|---|
| `ContextFirst.md` | Did I read before writing? Did I verify before proposing? |
| `Honesty.md` | Are there any unverified claims presented as facts? Any fabricated file paths, APIs, or structures? |
| `YAGNI.md` | Am I recommending things that aren't concretely needed right now? |
| `DRY.md` | Am I proposing something that duplicates what already exists? |

### 6. Phantom Detection

- [ ] **No phantom suggestions** — Every recommendation to "create X" is preceded by evidence that X does not already exist.
- [ ] **No redundant rules/skills** — If suggesting a new rule or skill, confirm it doesn't overlap with existing ones (including Constitution principles).

---

## When to Use This Skill

| Trigger | Action |
|---|---|
| User asks "what's missing / what do we need" | Full Pre-Flight (steps 1-3) + Post-Flight (steps 4-6) |
| Architecture review or gap analysis | Full Pre-Flight (steps 1-3) + Post-Flight (steps 4-6) |
| Recommending new files, rules, or skills | Steps 1, 2, 6 minimum |
| Any response with >3 factual claims about project | Steps 4, 5 minimum |
| Simple code fix or minor edit | Skip — overkill for trivial tasks |
