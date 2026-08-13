<!--
SYNC IMPACT REPORT
==================
Version change: Initial Template → 1.0.0
Modified principles:
  - Principle I: Spec-Driven Development (SDD) & Phase Scope Enforcement (Strict prohibition on modifying source code during specify/plan/tasks/analyze)
  - Principle II: Object-Oriented Programming (OOP) & SOLID Principles (Strict adherence to SOLID)
  - Principle III: Gang of Four (GoF) Design Patterns (Composite pattern mandatory for nested hierarchies)
  - Principle IV: Library-First Approach & Test-Driven Development (TDD) (Core hierarchy parsing & path generation as standalone libraries, TDD prior to UI integration)
  - Principle V: Self-Contained & Environment-Independent Excel Processing (No MS Excel app requirement)
Added sections: Workflow & Phase Controls, Governance
Removed sections: Template placeholder sections
Follow-up TODOs: None
-->

# Project Constitution

## Core Principles

### I. Spec-Driven Development (SDD) & Phase Scope Enforcement
- This project strictly follows Spec-Driven Development (SDD) methodology.
- **Strict Scope Prohibition**: The AI agent and developers are strictly prohibited from creating, editing, or deleting source code during the `specify`, `plan`, `tasks`, and `analyze` phases. Source code modifications are strictly reserved for the `implement` phase after specifications and task plans are finalized.

### II. Object-Oriented Programming (OOP) & SOLID Principles
- All software components must be designed using Object-Oriented Programming (OOP).
- Strict adherence to SOLID design principles is non-negotiable:
  - **Single Responsibility Principle (SRP)**: Each class/module must have only one reason to change.
  - **Open/Closed Principle (OCP)**: Software entities must be open for extension but closed for modification.
  - **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types.
  - **Interface Segregation Principle (ISP)**: Clients must not be forced to depend on interfaces they do not use.
  - **Dependency Inversion Principle (DIP)**: High-level modules must depend on abstractions, not concrete implementations.

### III. Gang of Four (GoF) Design Patterns
- Classic Gang of Four (GoF) design patterns must be applied where appropriate to solve structural, creational, and behavioral challenges cleanly.
- Structural hierarchies, nested nodes, and tree structures (such as folder/path trees and multi-level data nodes) **must** utilize the **Composite pattern** to unify leaf and container objects under a uniform interface.

### IV. Library-First Approach & Test-Driven Development (TDD)
- **Library-First**: All core business logic—specifically hierarchy parsing, data transformations, and path-generation logic—must be implemented as standalone, decoupled libraries before any UI integration.
- **TDD Requirement**: Unit tests must be written first and confirmed failing before writing the corresponding production logic (Red-Green-Refactor cycle).
- Libraries must be fully covered by comprehensive unit tests prior to UI assembly or integration.

### V. Self-Contained & Environment-Independent Excel Processing
- Excel document reading, writing, and parsing operations must be entirely self-contained.
- Excel processing **must run without requiring Microsoft Excel installation** or COM interop dependencies on the target host environment.

## Workflow & Phase Controls

1. **Specify Phase**: Create and clarify requirements in feature specifications (`spec.md`). No source code writing.
2. **Plan Phase**: Produce architectural decisions and research documents (`plan.md`). No source code writing.
3. **Tasks Phase**: Generate discrete, testable action items (`tasks.md`). No source code writing.
4. **Analyze Phase**: Validate alignment across spec, plan, and tasks. No source code writing.
5. **Implement Phase**: Write TDD tests, implement library/core logic, and assemble UI components.

## Governance
- This constitution supersedes all informal team conventions or ad-hoc practices.
- Every pull request, spec review, and task breakdown must be verified for compliance against these principles.

**Version**: 1.0.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-13
