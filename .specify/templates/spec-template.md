# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`

**Created**: [DATE]

**Status**: Draft

**Input**: User description: "$ARGUMENTS"

---

## 🗑️ Retirement & Cleanup Matrix *(mandatory for changes replacing existing logic)*

<!--
  MANDATORY GATE: Identify any components, RPC endpoints, models, adapter methods, or DOM widgets
  made obsolete or redundant by this feature. Specify their immediate deletion and test pruning.
-->

| Component / Endpoint / File | Action (Delete / Refactor / Migrate) | Replacement (Canonical New Approach) | Obsolete Tests to Remove / Update |
|---|---|---|---|
| *e.g., `old_rpc_method()`* | *Delete* | *`new_unified_rpc()`* | *`test_old_rpc.py` (Delete)* |
| *None (if purely additive)* | *N/A* | *N/A* | *N/A* |

---

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases & Red Teaming (Zero-Data & Error States)

<!--
  ACTION REQUIRED: Fill them out with zero-data scenarios, empty states, and boundary conditions.
-->

- What happens when [zero-data state / empty database / clean slate]?
- How does system handle [boundary condition / error scenario]?
- How is user deadlock prevented if elements are removed or relocated?

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [Test pass rate metric, e.g., "100% passing tests with zero zombie tests and zero warnings"]

---

## Assumptions

- [Assumption about target users, e.g., "Users have stable local files"]
- [Assumption about scope boundaries, e.g., "Feature strictly preserves existing system map contracts"]
- [Dependency on existing system/service, e.g., "Requires WorkspaceForest and HierarchyNode"]
