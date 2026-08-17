---
trigger: always_on
---

# SOLID Architectural Principles

> **Mandatory Policy:** All code design, refactoring, and implementations must adhere to SOLID principles. Avoid overengineering; apply principles proportionally to problem complexity.

## Core Directives

* **Single Responsibility (SRP):** Each module, class, or function must have only one reason to change. Separate business logic, data access, and UI/presentation concerns.
* **Open/Closed (OCP):** Software entities should be open for extension, but closed for modification. Use interfaces, abstractions, or composition instead of editing stable, working code.
* **Liskov Substitution (LSP):** Subtypes must be fully substitutable for their base types without altering program correctness. Avoid empty method overrides or throwing unexpected exceptions in derived classes.
* **Interface Segregation (ISP):** Prefer small, client-specific interfaces over large, general-purpose ones. Do not force classes to depend on methods they do not use.
* **Dependency Inversion (DIP):** Depend on abstractions, not on concrete implementations. High-level modules must not import low-level modules directly; inject dependencies explicitly.