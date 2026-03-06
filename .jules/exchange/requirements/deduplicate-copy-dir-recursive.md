---
label: "refacts"
implementation_ready: false
---

## Goal

Consolidate redundant implementations of `copy_dir_recursive` into a single shared capability to adhere to the Single Source of Truth principle.

## Problem

A recursive directory copy function is redundantly implemented in both `deploy_configs.rs` and `config/mod.rs`. This duplicates logic across boundaries, forcing future bug fixes or changes to be mirrored manually.

## Evidence

- source_event: "duplicate-copy-dir-recursive-data-arch.md"
  path: "src/app/commands/deploy_configs.rs"
  loc: "line 53"
  note: "Implements `copy_dir_recursive` publicly to support the `deploy_for_tags` function."

- source_event: "duplicate-copy-dir-recursive-data-arch.md"
  path: "src/app/commands/config/mod.rs"
  loc: "line 51"
  note: "Implements an almost identical private `copy_dir_recursive` function to support the `create` command."

## Change Scope

- `src/app/commands/deploy_configs.rs`
- `src/app/commands/config/mod.rs`
- `src/adapters/fs/` (or similar appropriate shared module)

## Constraints

- Duplicate logic must be consolidated to a single source of truth.

## Acceptance Criteria

- `copy_dir_recursive` is moved to a shared module.
- `deploy_configs.rs` and `config/mod.rs` both import and use the consolidated `copy_dir_recursive` function.
