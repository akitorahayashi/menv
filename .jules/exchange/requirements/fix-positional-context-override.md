---
label: "refacts"
implementation_ready: false
---

## Goal

Refactor the `make` command's `profile` argument from a positional argument to an explicit option to separate target objects from context overrides.

## Problem

The `make` command defines `profile` as a positional argument rather than an explicit option, violating the structural separation of target objects and context overrides, which creates a rigid, over-parameterized interface.

## Evidence

- source_event: "positional-context-override-cli-sentinel.md"
  path: "src/app/cli/make.rs"
  loc: "16-17"
  note: "The `profile` argument is defined as a positional string with a default value of 'common', functioning as an implicit context override rather than an explicit option (e.g., `--profile`)."

## Change Scope

- `src/app/cli/make.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- The `profile` parameter is parsed as an explicit flag (e.g., `--profile`) rather than a positional argument.
- The CLI structural separation of objects and options is maintained.
