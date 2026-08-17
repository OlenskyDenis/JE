---
name: design-patterns
description: >
  GoF Design Patterns reference and architectural best practices.
  Use when designing, refactoring, or reviewing architecture where structural patterns are relevant.
---

# GoF Design Patterns & Architectural Best Practices

> **Policy:** Apply standard Gang of Four (GoF) design patterns only when they naturally fit the architectural problem. Avoid forced pattern adoption.

## Core Directives

* **Purposeful Application:** Use Creational, Structural, and Behavioral patterns only to solve concrete decoupling, flexibility, or extensibility issues.
* **Composition Over Inheritance:** Prefer object composition and interface delegation over deep inheritance hierarchies (e.g., Strategy, Decorator, Adapter).
* **Encapsulate Variation:** Identify aspects of the code that vary frequently and isolate them behind abstractions (e.g., Factory Method, Command, Observer).
* **Idiomatic Implementation:** Adapt patterns to modern language idioms rather than copying classical, verbose boilerplate directly from book diagrams.
* **Anti-Pattern Prevention:** Do not turn simple objects into complex factories or god-singletons unnecessarily.

## Pattern Quick Reference

### Creational
| Pattern | When to Use |
|---|---|
| Factory Method | Object creation varies by subtype |
| Abstract Factory | Families of related objects |
| Builder | Complex object construction with many optional parts |
| Singleton | Single shared resource (use sparingly) |

### Structural
| Pattern | When to Use |
|---|---|
| Adapter | Bridge incompatible interfaces |
| Decorator | Add behavior without modifying the original class |
| Facade | Simplify a complex subsystem |
| Proxy | Lazy loading, access control, logging |

### Behavioral
| Pattern | When to Use |
|---|---|
| Strategy | Interchangeable algorithms |
| Observer | Event-driven, decoupled notifications |
| Command | Encapsulate operations for undo/redo or queuing |
| Template Method | Shared algorithm skeleton, variable steps |

## Decision Checklist

Before applying a pattern, confirm:
- [ ] Does the problem involve a concrete variation or extension point?
- [ ] Would the pattern reduce coupling between components?
- [ ] Is the pattern idiomatic for the language/framework?
- [ ] Is the added abstraction justified by current (not future) complexity?
