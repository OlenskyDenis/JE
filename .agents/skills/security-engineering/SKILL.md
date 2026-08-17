---
name: security-engineering
description: >
  Detailed security and defensive engineering guidelines.
  Use when implementing authentication, authorization, data handling, API design, or any security-sensitive feature.
---

# Security & Defensive Engineering — Detailed Guide

> **Policy:** Apply defense-in-depth and least privilege across all layers. Security is non-negotiable.

## Input Validation & Sanitization

* Validate **type, length, format, and range** at every system boundary (API endpoints, CLI args, file uploads).
* Use **allowlists**, not denylists — define what is valid, reject everything else.
* Never construct SQL, shell commands, or HTML from raw user input — use parameterized queries and safe templating.
* Treat all external data as untrusted: HTTP headers, query params, request bodies, cookies, environment variables.

### Common Injection Vectors

| Attack | Prevention |
|---|---|
| SQL Injection | Parameterized queries / ORMs |
| XSS | Output encoding, CSP headers |
| Command Injection | Avoid shell calls; use safe APIs |
| Path Traversal | Canonicalize and whitelist allowed paths |
| CSRF | SameSite cookies, CSRF tokens |

## Secret Management

> The two core invariants (no hardcoded secrets, validate all input) are enforced by `Security.md`. This section covers operational details only.

* Load secrets from environment variables or a dedicated secrets manager (Vault, AWS SSM, etc.).
* Exclude `.env` files and credential stores from version control via `.gitignore`.
* Rotate secrets regularly; invalidate leaked secrets immediately.

## Authentication & Authorization

* Use **short-lived tokens** (JWT with expiry, session tokens) over long-lived credentials.
* Apply **least privilege**: grant only the minimum permissions required for operation.
* Enforce authorization checks **server-side** — never trust client-provided roles or permissions.
* Implement proper session invalidation on logout.

## Data Privacy & Redaction

* Mask PII, tokens, and credentials in all logs, error messages, and telemetry.
* Do not log request bodies containing sensitive fields (passwords, card numbers).
* Apply data minimization — only collect and retain data that is strictly necessary.

## Dependency Safety

* Avoid outdated or vulnerable third-party packages — audit regularly with `npm audit`, `pip-audit`, `trivy`, etc.
* Favor vetted standard libraries for cryptographic operations over custom implementations.
* Pin dependency versions in production; avoid broad version ranges (`*`, `^latest`).

## Secure Defaults Checklist

- [ ] HTTPS enforced for all endpoints
- [ ] Sensitive headers set (HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Error responses do not expose stack traces or internal paths
- [ ] File uploads validated by content type (not just extension)
- [ ] Rate limiting applied to authentication endpoints
