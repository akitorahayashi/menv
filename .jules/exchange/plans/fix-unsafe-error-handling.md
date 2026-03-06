---
label: "bugs"
---

## Goal

Eliminate unsafe error handling practices, specifically the use of `unwrap()` and silent fallbacks like `unwrap_or()` across the codebase.

## Problem

The codebase relies on `unwrap()` and `unwrap_or()` in multiple adapters, commands, and tests. This causes silent fallbacks that obscure invalid states and context loss, or panic traces instead of surfacing the underlying `Result` failure context. Errors must be part of the contract and explicitly propagated or handled.

## Affected Areas

### Error Handling Updates

- `src/adapters/ansible/executor.rs`
- `src/app/commands/backup/mod.rs`
- `src/domain/profile.rs`

## Constraints

- Errors must be part of the contract. Proper Result propagation or explicit matching is required.
- Unsafe usages of `unwrap()` and `expect()` are strictly prohibited.
- Silent fallbacks are prohibited.

## Risks

- Changing `unwrap_or()` to explicit error propagation might bubble up errors to callers that were previously unaffected, requiring updates to function signatures and call sites.
- Tests may need adjustments if new errors are propagated instead of handled silently.

## Acceptance Criteria

- No instances of `unwrap_or()` masking errors in `src/adapters/ansible/executor.rs`.
- No instances of `unwrap_or()` masking errors in `src/app/commands/backup/mod.rs`.
- No instances of `unwrap()` in test bodies in `src/domain/profile.rs`; tests should propagate errors.

## Implementation Plan

1. Execute `replace_with_git_merge_diff` on `src/adapters/ansible/executor.rs` to match on `self.ansible_dir.parent()` and return `AppError::AnsibleExecution` if it is `None`, instead of using `unwrap_or(Path::new("."))`.
2. Execute `replace_with_git_merge_diff` on `src/adapters/ansible/executor.rs` to explicitly match on `status.code()`. If `Some(code)`, use it in the error message; if `None`, state "exited with unknown code" instead of using `unwrap_or(-1)`.
3. Execute `run_in_bash_session` with `cat src/adapters/ansible/executor.rs` to verify the changes.
4. Execute `replace_with_git_merge_diff` on `src/app/commands/backup/mod.rs` to update `format_value` to return `Result<String, AppError>`. Replace `serde_json::to_string(&value).unwrap_or(value)` with a match or explicit error mapping, returning `AppError::Backup` on failure.
5. Execute `replace_with_git_merge_diff` on `src/app/commands/backup/mod.rs` to update `format_numeric` to return `Result<String, AppError>`. Replace `unwrap_or` calls on `target.parse::<f64>()` with explicit matching and return `AppError::Backup` if parsing fails.
6. Execute `replace_with_git_merge_diff` on `src/app/commands/backup/mod.rs` to update `format_string` to return `Result<String, AppError>`. Replace `serde_json::to_string(&value).unwrap_or(value)` with `map_err` to return `AppError::Backup`.
7. Execute `replace_with_git_merge_diff` on `src/app/commands/backup/mod.rs` to update the `execute_system` function where `format_value` is called. Add `?` to `format_value(def, &raw_value)?` since `format_value` now returns a `Result`.
8. Execute `run_in_bash_session` with `cat src/app/commands/backup/mod.rs` to verify the changes.
9. Execute `replace_with_git_merge_diff` on `src/domain/profile.rs` to change the signature of `validate_machine_profile_accepts_macbook` to return `Result<(), AppError>` and replace `.unwrap()` with `?`.
10. Execute `run_in_bash_session` with `cat src/domain/profile.rs` to verify the test change.
11. Execute `run_in_bash_session` with `cargo test` to ensure all tests pass and no regressions were introduced.
12. Execute `run_in_bash_session` with `rg -e "unwrap\(" -e "unwrap_or\(" src/adapters/ansible/executor.rs src/app/commands/backup/mod.rs src/domain/profile.rs` and expect no results to verify removal.