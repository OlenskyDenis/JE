---
trigger: always_on
---

# Security — Core Invariants

> **Mandatory Policy:** Two rules that apply to every task, always.

* **Never hardcode secrets.** API keys, tokens, passwords, and credentials must come from environment variables or a secrets manager — never from source code or config files committed to version control.
* **Never trust external input.** Validate, sanitize, and strongly type all data at system boundaries. Use parameterized queries, safe templating, and allowlists.

> For detailed guidance (XSS, CSRF, auth patterns, dependency auditing), load the `security-engineering` skill.