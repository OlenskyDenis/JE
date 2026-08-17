# Feature Specification: Full-Stack Use Case Lifecycle Diagrams & Test Verification Checklists

**Feature Branch**: `035-use-case-diagrams-and-test-checklists`

**Created**: 2026-08-17

**Status**: Draft

**Input**: User description: "Потрібно для кожної сутності по типу налаштування, переклад мови, різні режими, створити діаграми варіантів використання, де буде показаний повний цикл її роботи як бек-енду так і паралельно фронт-енду, і відповідно до цих діаграм варіантів використання потрібно створити чек-листи які і будуть слугувати перевіркою чи пройшли тести успішно з точки зору чи всі варіанти вони пройшли."

---

## 💡 Clarifications

### Session 2026-08-17
- **Q**: Які саме сутності та підсистеми повинні бути покриті діаграмами та чек-листами?
  **A**: 6 ключових підсистем проекту: Налаштування, Локалізація i18n, 3 Режими перегляду, Життєвий цикл книги Excel/Multi-sheet, Дерево CRUD/Drag-Drop, Уніфікований сайдбар.
- **Q**: Який формат структуризації діаграм та чек-листів верифікації обрати?
  **A**: **Ієрархічна системна карта компонентів та взаємодій (Hierarchical System Map & Component Lifecycle Architecture)**:
  1. **Рівень А (Атомарні мікро-цикли)**: Менші елементи описуються як повноцінні самостійні цикли роботи (`ButtonActionLifecycle`, `ModalLifecycle`, `InputSearchLifecycle`, `SelectDropdownLifecycle`, `BadgeCounterLifecycle`, `ResizerHandleLifecycle`, `ToastNotificationLifecycle`).
  2. **Рівень Б (Макро-конструкції / Системні сценарії)**: Більші підсистеми взаємодіють, посилаючись на назви цих атомарних циклів як на будівельні блоки у наскрізних Mermaid-діаграмах паралельної взаємодії Frontend $\leftrightarrow$ Backend.
  3. **Рівень В (Нормативні чек-листи)**: Чек-листи формуються за ієрархією з прямою прив'язкою до існуючих автоматизованих тестів у `tests/`.

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| Неструктуровані або розрізнені описи сценаріїв | Migrate / Standardize | Єдиний нормативний комплект архітектурних Mermaid-діаграм повного циклу та нормативних чеклистів верифікації | `docs/KNOWLEDGE.md`, `specs/035-*/` |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full-Stack Sequence & State Lifecycle Diagrams (Priority: P1) 🎯 MVP

As a system architect and developer, I want clear, end-to-end Mermaid sequence and state lifecycle diagrams depicting the parallel execution flow between Frontend controllers/DOM and Backend Python services/Eel RPC for each core entity, so that interaction boundaries and state transitions are transparent and unambiguous.

**Why this priority**: Without explicit lifecycle maps, frontend and backend state transitions can diverge, causing subtle state mismatch bugs.

**Independent Test**: Review `specs/035-use-case-diagrams-and-test-checklists/diagrams.md` and verify syntax rendering of all 6 full-stack Mermaid diagrams covering both Frontend and Backend layers.

**Acceptance Scenarios**:
1. **Given** Settings entity, **When** reviewing its diagram, **Then** it clearly shows the sequence from UI open $\to$ delimiter edit $\to$ RPC `update_settings` $\to$ `SettingsService` storage $\to$ tree recalculation $\to$ UI leaf paths re-render.
2. **Given** Multi-Sheet Session entity, **When** reviewing its diagram, **Then** it shows file selection $\to$ streaming openpyxl reader $\to$ session forest dict $\to$ active/catalog sheet selectors population $\to$ dirty state tracking $\to$ unsaved modal prompt.
3. **Given** View Modes entity, **When** reviewing its diagram, **Then** it shows mode selection $\to$ ViewModeManager class toggles $\to$ Tree / Matrix table / Unique Levels grouping algorithms $\to$ synchronized hover highlights.

---

### User Story 2 - Exhaustive Verification Checklists & State Coverage Matrices (Priority: P1)

As a QA lead and automation engineer, I want formal, itemized verification checklists for each use case diagram containing exact pre-conditions, trigger actions, expected frontend DOM states, expected backend RPC states, and direct links to automated tests, so that 100% of functional paths are proven to be covered without blind spots.

**Why this priority**: Checklists provide the definitive source of truth for test completeness and eliminate guesswork.

**Independent Test**: Review `specs/035-use-case-diagrams-and-test-checklists/checklists.md` and verify that every branch and edge case in the diagrams has a corresponding checklist item mapped to an automated test in `tests/`.

**Acceptance Scenarios**:
1. **Given** each checklist item, **When** inspected, **Then** it specifies: ID, Pre-condition, Action Trigger, Frontend Verification, Backend Verification, and Mapped Test Case.
2. **Given** the complete checklist matrix, **When** audited against `pytest`, **Then** 100% of checklist items are proven to have active, passing automated tests.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide full-stack Mermaid sequence diagrams for all 6 core functional entities: Settings, i18n Localization, Multi-Sheet Sessions, View Modes, Tree CRUD & Drag-Drop, and Unified Sidebar.
- **FR-002**: Each diagram MUST depict both Frontend (DOM events, controllers, visual feedback) and Backend (Eel RPC, services, models, adapters) lifecycles in parallel.
- **FR-003**: System MUST provide formal, itemized verification checklists derived directly from each diagram.
- **FR-004**: Every checklist item MUST specify Pre-conditions, Action, Expected Frontend State (visibility, classes, values), Expected Backend State, and Mapped Test Path.
- **FR-005**: All generated documentation files MUST adhere to the Constitution Principle VIII ($\le 200$ lines per modular file where applicable or logically structured).
- **FR-006**: The checklist matrix MUST verify that 100% of documented branches are covered by existing automated tests in `tests/e2e/`, `tests/matrix/`, `tests/integration/`, or `tests/unit/`.

---

### Key Entities

- **LifecycleDiagrams (`specs/035-*/diagrams.md`)**: Visual Mermaid diagrams modeling full-stack interaction sequences.
- **VerificationChecklists (`specs/035-*/checklists.md`)**: Tabular and checklist verification specifications mapped to automated tests.
- **CoverageTraceabilityMatrix (`specs/035-*/traceability_matrix.md`)**: Direct mapping between functional requirements, use-case branches, and test assertions.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 6 complete, syntactically valid Mermaid lifecycle sequence diagrams documenting 100% of core system entities.
- **SC-002**: 100% of diagram branches, error states, and transitions have corresponding items in the verification checklists.
- **SC-003**: 100% traceability: every checklist item maps to a concrete, passing automated test in the JE test suite.
- **SC-004**: Quality gate execution (`python scripts/check_all.py --full`) confirms 100% test pass rate with zero errors.
