<!--
SYNC IMPACT REPORT
==================
Version change: 1.5.0 → 1.6.0
Modified principles:
  - Principle I: Spec-Driven Development (SDD) & Phase Scope Enforcement
  - Principle II: Object-Oriented Programming (OOP), SOLID Principles, Strict YAGNI & Downward-Only Dependency Flow
  - Principle III: Gang of Four (GoF) Design Patterns (Dynamic Composite pattern mandatory for nested hierarchies)
  - Principle IV: Library-First Approach, Test-Driven Development (TDD) & Test-Code Parity Gate
  - Principle V: Self-Contained & Environment-Independent Excel Processing (No MS Excel app requirement)
  - Principle VI (AMENDED): Mandatory Modular System Map First-Load, Context Router Navigation, Full Dependency Tracing, Proactive Redundancy Audit & Retirement Verification Gate (Mandatory first-step loading of .specify/system_map.md Master Router and domain-targeted loading of .specify/system_map/*.md modular maps)
  - Principle VII: Proactive Specification Red Teaming & Zero-Data / Empty-State Stress Testing
Added sections: Modular System Map Router navigation in Principle VI and Workflow Controls
Removed sections: None
Follow-up TODOs: None
-->

# Project Constitution

## Core Principles

### I. Spec-Driven Development (SDD) & Phase Scope Enforcement
- This project strictly follows Spec-Driven Development (SDD) methodology.
- **Strict Scope Prohibition**: The AI agent and developers are strictly prohibited from creating, editing, or deleting source code during the `specify`, `plan`, `tasks`, and `analyze` phases. Source code modifications are strictly reserved for the `implement` phase after specifications and task plans are finalized.

### II. Object-Oriented Programming (OOP), SOLID Principles & Domain Isolation
- All software components must be designed using Object-Oriented Programming (OOP).
- Strict adherence to SOLID design principles is non-negotiable:
  - **Single Responsibility Principle (SRP)**: Each class/module must have only one reason to change.
  - **Open/Closed Principle (OCP)**: Software entities must be open for extension but closed for modification. Centralized domain enumerations and types (e.g. `data_types.py`) must be used rather than duplicated across modules.
  - **Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types.
  - **Interface Segregation Principle (ISP)**: Clients must not be forced to depend on interfaces they do not use.
  - **Dependency Inversion Principle (DIP) & Downward-Only Dependency Flow**:
    * Dependencies across the codebase must flow **strictly downward**: `Frontend / UI -> RPC Bridge -> Application Services -> Domain Models`.
    * Domain models (`src/hierarchy_lib/models/`) are pure domain abstractions and **MUST NEVER import or depend on** services (`services/`), adapters (`adapters/`), or persistence configuration managers (`SettingsService`). Models must receive configuration values (such as delimiters or default types) as pure method parameters with self-contained defaults.
  - **Strict YAGNI & Direct Sunset**:
    * Whenever a new architectural approach or unified RPC replaces older logic, the superseded code, endpoints, methods, and files **MUST be completely deleted in the same feature iteration**.
    * Accumulation of "phantom" deprecated wrappers, backwards-compatible empty aliases, or dead code paths is strictly forbidden.

### III. Gang of Four (GoF) Design Patterns
- Classic Gang of Four (GoF) design patterns must be applied where appropriate to solve structural, creational, and behavioral challenges cleanly.
- Structural hierarchies, nested nodes, and tree structures (such as folder/path trees and multi-level data nodes) **must** utilize the **Composite pattern** (via dynamic `HierarchyNode`) to unify leaf and container objects under a uniform interface.

### IV. Library-First Approach, Test-Driven Development (TDD) & Test-Code Parity Gate
- **Library-First**: All core business logic—specifically hierarchy parsing, data transformations, and path-generation logic—must be implemented as standalone, decoupled libraries before any UI integration.
- **TDD Requirement**: Unit tests must be written first and confirmed failing before writing the corresponding production logic (Red-Green-Refactor cycle).
- **Test-Code Parity Gate (No Zombie Tests)**:
  * Tests must strictly reflect active, current functionality.
  * When code or RPC endpoints are deleted or replaced, any tests asserting that deleted behavior **must be deleted or migrated simultaneously**.
  * Keeping zombie tests that assert obsolete or non-functional legacy behaviors is strictly forbidden.
  * All test suites must execute with 100% pass rate and zero third-party warning pollution.

### V. Self-Contained & Environment-Independent Excel Processing
- Excel document reading, writing, and parsing operations must be entirely self-contained.
- Excel processing **must run without requiring Microsoft Excel installation** or COM interop dependencies on the target host environment, utilizing streaming read-only mode for high performance.

### VI. Mandatory Modular System Map First-Load, Context Router Navigation & Retirement Verification Gate
- **Mandatory First Action & Router Navigation**: For every new feature, change, or bug fix, the AI agent **MUST load and read [`.specify/system_map.md`](../system_map.md) (Master Router Hub) as the very first step**. Depending on the domain of the feature, the agent must then selectively load the relevant modular map(s) in [`.specify/system_map/`](../system_map/):
  * `domain_and_models.md` for pure domain models, data types, and tree manipulations.
  * `views_and_ui.md` for HTML layout, CSS styling, renderers, and DOM interactions.
  * `controllers_and_rpc.md` for JS controller actions and Eel RPC bridge endpoints.
  * `dtos_and_contracts.md` for JSON DTO wire schemas and response formats.
  * `infrastructure_and_adapters.md` for openpyxl I/O, OS dialogs, and file persistence.
  * `state_and_lifecycle.md` for multi-sheet session state and dirty flag lifecycle.
  * `tests_and_quality.md` for test registry and architecture linters.
- **Full Cross-Layer Dependency Tracing**: The agent must trace all upstream and downstream dependencies across the active architecture layers before formulating changes.
- **Proactive Redundancy & Conflict Detection (Pre-Spec Gate)**: **BEFORE** proposing specifications or plans, the agent must actively inspect and identify obsolete UI elements, duplicate logic, or dead endpoints and populate the Retirement & Cleanup Matrix.
- **Retirement Verification Gate**: Before deleting or retiring any backend class, service, RPC endpoint, or frontend controller method, the agent must perform comprehensive cross-layer verification across all source files and test suites. Referencing call sites or obsolete assertions must be migrated or pruned simultaneously.
- **Continuous System Map Synchronization**: Whenever any component, model, endpoint, or UI widget is created, modified, or retired, the master router and affected modular maps in `.specify/system_map/` must be updated immediately.

### VII. Proactive Specification Red Teaming & Zero-Data / Empty-State Stress Testing
- **No Blind Acceptance**: The AI agent and specification architects must **never blindly accept UI/UX changes, element removals, or workflow redesigns** without critical analysis.
- **Mandatory Red Teaming**: For every proposed feature, button relocation, or element deletion, the agent must actively stress-test and simulate alternative user journeys before proceeding to planning.
- **Clean-Slate & Empty-State Analysis**: Systematically evaluate:
  1. *Zero-Data Scenarios*: How does a user interact when starting from scratch with 0 files loaded, an empty database, or empty sessions?
  2. *User Deadlock / Dead-End Detection*: Does removing or altering an element trap the user in a state where necessary actions (such as initial entity creation or offline modeling) become impossible?
  3. *Fault & Offline Tolerance*: Are graceful fallbacks in place for empty sheets, network disconnections, or dialog cancellations?
- **Immediate Flagging & Solution Proposals**: If an architectural conflict, user deadlock, or UX regression is discovered during Red Teaming, the agent must proactively flag it to the user and propose alternative designs (e.g. contextual action triggers in empty states) prior to finalizing the plan.

---

## Workflow & Phase Controls

1. **Specify Phase**:
   - **Step 1 (First Action)**: Load and read [`.specify/system_map.md`](../system_map.md) (Router Hub) and consult the relevant modular maps in [`.specify/system_map/`](../system_map/). Trace all component dependencies.
   - **Step 2**: Proactively audit and flag any obsolete, redundant, or conflicting UI elements / code logic. Populate the Retirement & Cleanup Matrix.
   - **Step 3**: Perform **Red Teaming & Zero-Data Stress Testing** (Principle VII) to verify clean-slate usability and prevent deadlocks.
   - **Step 4**: Create and clarify requirements in feature specifications (`spec.md`). No source code writing.
2. **Plan Phase**:
   - Produce architectural decisions, component contracts, and research documents (`plan.md`).
   - Re-verify Red Teaming findings and update the relevant modular maps in [`.specify/system_map/`](../system_map/). No source code writing.
3. **Tasks Phase**:
   - Generate discrete, testable action items (`tasks.md`), including edge case test coverage and hygiene cleanup tasks. No source code writing.
4. **Analyze Phase**:
   - Validate alignment across spec, plan, tasks, system map, and Red Teaming guarantees. No source code writing.
5. **Implement Phase**:
   - Write TDD tests, implement library/core logic, assemble UI components, and verify system map consistency.

---

## Governance
- This constitution supersedes all informal team conventions or ad-hoc practices.
- Every pull request, spec review, and task breakdown must be verified for compliance against these principles.

**Version**: 1.6.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-16
