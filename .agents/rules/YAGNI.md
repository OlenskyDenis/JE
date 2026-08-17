---
trigger: always_on
---

# YAGNI Principle (You Aren't Gonna Need It)

> **Mandatory Policy:** Implement only what is explicitly required by current requirements. Speculative coding for hypothetical future needs is prohibited.

## Core Directives

* **No Speculative Architecture:** Do not create interfaces, generic layers, or configuration options until there is a concrete, current need for them.
* **Just-In-Time Implementation:** Write code strictly to solve today's problem. Extend and refactor the architecture only when new requirements actually emerge.
* **Minimal API Surface:** Expose only the methods, properties, and parameters that are actively consumed. Avoid adding unused helper methods "just in case".
* **Zero Dead Scaffolding:** Do not leave placeholder functions, empty stubs, or commented-out code intended for future features.