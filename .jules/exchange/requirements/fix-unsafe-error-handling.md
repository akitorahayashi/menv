---
label: "bugs"
implementation_ready: false
---

## Goal

Eliminate unsafe error handling practices, specifically the use of `unwrap()` and silent fallbacks like `unwrap_or()` across the codebase.

## Problem

The codebase relies on `unwrap()` and `unwrap_or()` in multiple adapters, commands, and tests. This causes silent fallbacks that obscure invalid states and context loss, or panic traces instead of surfacing the underlying `Result` failure context. Errors must be part of the contract and explicitly propagated or handled.

## Evidence

- source_event: "ansible-executor-unwrap-or-rustacean.md"
  path: "src/adapters/ansible/executor.rs"
  loc: "line 82, 107"
  note: "Silently defaults repo path and exit codes on failure."

- source_event: "backup-command-unwrap-rustacean.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "line 169, 204, 208, 229"
  note: "Silently ignores serialization and floating point parsing errors."

- source_event: "profile-test-unwrap-rustacean.md"
  path: "src/domain/profile.rs"
  loc: "line 123, 124"
  note: "Uses `unwrap()` directly in the test body instead of correctly propagating errors."

## Change Scope

- `src/adapters/ansible/executor.rs`
- `src/app/commands/backup/mod.rs`
- `src/domain/profile.rs`

## Constraints

- Errors must be part of the contract. Proper Result propagation or explicit matching is required.
- Unsafe usages of `unwrap()` and `expect()` are strictly prohibited.
- Silent fallbacks are prohibited.

## Acceptance Criteria

- No instances of `unwrap_or()` masking errors in the specified files.
- No instances of `unwrap()` in test bodies; tests should propagate errors.
