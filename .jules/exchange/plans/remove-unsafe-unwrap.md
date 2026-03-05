---
label: "bugs"
---

## Goal

Replace unsafe `unwrap()` and `expect()` usages in `mev-internal` CLI commands and tests with proper Result propagation.

## Problem

The CLI commands in `mev-internal` use `unwrap()` and `expect()` directly, especially around JSON parsing and filesystem operations, bypassing proper error handling and propagation which violates the principle of "errors are part of the contract".

## Affected Areas

### CLI Commands
- `crates/mev-internal/src/app/cli/shell.rs`
- `crates/mev-internal/src/app/cli/ssh.rs`

### Domain
- `src/domain/profile.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- Silent fallbacks are prohibited; any fallback is explicit, opt-in, and surfaced as a failure or a clearly logged, reviewed decision.

## Risks

- Changing `unwrap()` to `Result` or explicit matching might require adjusting function signatures in tests or application code.
- Removing `unwrap()` might expose errors that were previously masked as panics, potentially causing CI failures if proper handling is not applied.

## Acceptance Criteria

- Proper error propagation (`?`) or explicit handling replaces `unwrap()` around JSON parsing and filesystem operations.
- Fallbacks and failures are explicit rather than panics.
- Tests are updated to either use `?` (returning `Result<(), Box<dyn std::error::Error>>`) or use explicit `match`/`assert!` statements instead of `.unwrap()`.

## Implementation Plan

1. Modify `crates/mev-internal/src/app/cli/shell.rs`:
   - Update `gen_vscode_workspace_in_dir` to handle `output_path.file_name()` safely instead of unwrap.
   - Update tests `gen_vscode_workspace_creates_file_with_expected_folders` to use `?` or safe matching instead of `.unwrap()`.

2. Modify `crates/mev-internal/src/app/cli/ssh.rs`:
   - Update tests `list_hosts_succeeds_when_conf_dir_absent` to handle the `Result` from `tempfile::tempdir()` and `collect_hosts()` using `?` by changing the test signature to return `Result<(), Box<dyn std::error::Error>>`.

3. Modify `src/domain/profile.rs`:
   - Update tests `validate_machine_profile_accepts_macbook` to replace `.unwrap()` with `assert_eq!(validate_machine_profile("macbook"), Ok("macbook"));`.
