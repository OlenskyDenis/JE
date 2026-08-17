---
trigger: always_on
---

# Error Handling, Resilience & Failure Management

> **Mandatory Policy:** Errors must never fail silently. Handle failures explicitly, safely, and predictably across all layers.

## Core Directives

* **Fail-Fast Principle:** Validate inputs, state invariants, and pre-conditions immediately at system boundaries. Fail as early as possible rather than propagating corrupted state.
* **No Silent Swallowing:** Never use empty `catch` blocks or suppress exceptions without explicit, documented fallback logic. Log or rethrow errors with actionable context.
* **Explicit Failure Contracts:** Prefer explicit error representations (Result types, domain-specific exceptions) over ambiguous return values like `null`, `false`, or `-1`.
* **Safe Degradation & Recovery:** Implement graceful fallbacks, retries with exponential backoff, and circuit breakers for external network or transient infrastructure failures.
* **Context-Rich Diagnostics:** Include relevant operational metadata (IDs, attempted operations, state) in error messages without exposing sensitive data (tokens, passwords, PII).
* **Cleanup & Resource Safety:** Guarantee the release of resources (connections, file handles, memory locks) using `try-finally`, `using`, or automated resource management patterns.