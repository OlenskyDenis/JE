---
trigger: always_on
---

# Context-First Principle

> **Mandatory Policy:** Read before you write. Verify before you propose.

## Core Directives

* **Read Existing Code First:** Before modifying, adding to, or refactoring any file — read it in full. Never assume its contents from filename or past memory.
* **Verify Before Proposing:** Before suggesting a new rule, file, function, or dependency — confirm it does not already exist in the codebase, config, or active context.
* **Check Active Context:** Loaded rules, open files, KI summaries, and chat history are authoritative. Cross-reference them before any recommendation.
* **No Phantom Suggestions:** Never propose creating something that is already present. Violating this rule is a direct breach of `Honesty.md`.
