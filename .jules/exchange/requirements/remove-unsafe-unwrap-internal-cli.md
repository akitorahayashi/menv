---
label: "bugs"
implementation_ready: false
---

## Goal

Replace unsafe `unwrap()` and `expect()` usages in `mev-internal` CLI commands and tests with proper Result propagation.

## Problem

The CLI commands in `mev-internal` use `unwrap()` and `expect()` directly, especially around JSON parsing and filesystem operations, bypassing proper error handling and propagation which violates the principle of "errors are part of the contract".

## Evidence

- source_event: "avoid-unsafe-unwrap-mev-internal-rustacean.md"
  path: "crates/mev-internal/src/app/cli/shell.rs"
  loc: "line 85"
  note: "`output_path.file_name().unwrap().to_string_lossy()` assumes the output path will always have a valid file name which could panic."
- source_event: "avoid-unsafe-unwrap-mev-internal-rustacean.md"
  path: "crates/mev-internal/src/app/cli/ssh.rs"
  loc: "line 265, 267"
  note: "Using `unwrap()` on `tempfile::tempdir()` and `collect_hosts` in tests hides failure modes instead of using proper `Result` propagation or more explicit assertions."
- source_event: "avoid-unsafe-unwrap-mev-internal-rustacean.md"
  path: "src/domain/profile.rs"
  loc: "line 82, 83"
  note: "Tests in domain profile contain multiple `unwrap()` usages directly."

## Change Scope

- `crates/mev-internal/src/app/cli/shell.rs`
- `crates/mev-internal/src/app/cli/ssh.rs`
- `src/domain/profile.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- Proper error propagation (`?`) or explicit handling replaces `unwrap()` around JSON parsing and filesystem operations.
- Fallbacks and failures are explicit rather than panics.
