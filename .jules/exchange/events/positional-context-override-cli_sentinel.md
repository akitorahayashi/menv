---
created_at: "2026-03-04"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

The `make` command defines `profile` as a positional argument rather than an explicit option, violating the structural separation of target objects and context overrides, which creates a rigid, over-parameterized interface.

## Evidence

- path: "src/app/cli/make.rs"
  loc: "16-17"
  note: "The `profile` argument is defined as a positional string with a default value of 'common', functioning as an implicit context override rather than an explicit option (e.g., `--profile`)."
