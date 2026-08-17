---
trigger: always_on
---

# DRY Principle (Don't Repeat Yourself)

> **Mandatory Policy:** Every piece of knowledge, logic, or data definition must have a single, unambiguous, authoritative representation within the system.

## Core Directives

* **Single Source of Truth:** Eliminate duplicate business logic, configurations, database schemas, and documentation. Define data and rules in one authoritative place.
* **Unified Logic Extraction:** Extract duplicated code blocks or identical algorithmic logic into reusable functions, modules, or services.
* **Atomic & Predictable Changes:** Design components so that modifying a single behavior requires changing only one place without causing cascading side effects.
* **Knowledge Over Syntax:** Focus on deduplicating business logic and domain knowledge, not just superficial code similarities. Avoid coupling unrelated features purely for code reduction.