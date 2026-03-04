---
created_at: "2026-03-04"
author_role: "devops"
confidence: "high"
---

## Statement

CI workflows use `brew install` for toolchain components without specifying specific versions or relying on a lockfile. This introduces non-determinism, as the installed versions depend on the current Homebrew catalog rather than the project's source of truth.

## Evidence

For multi-file events, add multiple list items.

- path: ".github/workflows/run-linters.yml"
  loc: "23"
  note: "Installs `shellcheck` and `shfmt` via `brew install` without version pinning."
- path: ".github/workflows/collect-coverage.yml"
  loc: "32"
  note: "Installs `mise` via `brew install` without version pinning."
