---
created_at: "2026-03-06"
author_role: "devops"
confidence: "high"
---

## Statement

CI workflows install system packages dynamically via package managers without pinning exact versions, introducing non-determinism and potential execution instability due to unverified upstream changes.

## Evidence

- path: ".github/workflows/run-linters.yml"
  loc: "line 20"
  note: "Runs `brew install shellcheck shfmt` without specifying toolchain versions."
- path: ".github/workflows/collect-coverage.yml"
  loc: "line 29"
  note: "Runs `brew install mise` without specifying a tool version."
