---
label: "tests"
---

## Goal

Improve test granularity, address 0% coverage gaps in critical modules, implement isolated filesystem boundaries for tests, and align the CI coverage gate with realistic metrics.

## Problem

The codebase relies heavily on slow, full-binary CLI integration tests rather than fine-grained unit behavior assertions. Standard filesystem operations rely directly on `std::fs` without mocked I/O boundaries, causing uncontrolled side effects. Significant portions of core CLI commands and external binary orchestrators have 0% line coverage. The CI `tarpaulin` coverage gate fails because the threshold (40%) exceeds the actual baseline (19.11%).

## Affected Areas

### I/O and Core Adapters
- `src/adapters/fs/std_fs.rs`
- `src/adapters/identity_store/local_json.rs`

### Commands and Business Logic
- `src/app/commands/deploy_configs.rs`
- `src/app/commands/switch/mod.rs`
- `src/app/commands/create/mod.rs`
- `src/app/commands/backup/mod.rs`
- `src/domain/execution_plan.rs`

### External Binary Orchestrators
- `crates/mev-internal/src/app/cli/aider.rs`
- `crates/mev-internal/src/app/cli/ssh.rs`

### Testing and CI
- `tests/cli/help_and_version.rs`
- `tests/cli/backup.rs`
- `tests/harness/test_context.rs`
- `justfile`

## Constraints

- I/O boundary components must be isolated and testable.
- Unit behavior must be asserted independently of full binary execution.
- Coverage threshold checks must align with the current baseline to avoid persistent CI failures.

## Risks

- Over-mocking standard I/O behavior might lead to false positive unit tests if edge cases are missed.
- Lowering the CI coverage gate might reduce test stringency in the short term, but accurately reflecting the baseline is necessary to get a passing CI signal to iterate from.

## Acceptance Criteria

- Unit tests exist for core command modules and internal external-binary orchestrators using `#cfg[(test)]` blocks.
- I/O behavior during tests is bounded without relying purely on standard filesystem modifications.
- The `justfile` `cargo tarpaulin` coverage threshold is adjusted to match the current achievable baseline, allowing CI to pass, or coverage is raised sufficiently.

## Implementation Plan

1. Adjust `justfile` to lower the `cargo tarpaulin` minimum threshold to 19%.
2. Create unit tests for `src/adapters/fs/std_fs.rs` testing behavior of the FsPort impl.
3. Create unit tests for `src/adapters/identity_store/local_json.rs` mocking filesystem using temp files and directory setup.
4. Refactor `deploy_configs.rs` logic to inject dependencies to allow bounded isolated test coverage of core functionality.
5. Create unit tests for `src/app/commands/switch/mod.rs` passing a mocked dependency container.
6. Create unit tests for `src/app/commands/create/mod.rs` passing a mocked dependency container.
7. Create unit tests for `src/app/commands/backup/mod.rs` passing a mocked dependency container.
8. Create unit tests for `src/domain/execution_plan.rs` checking if `full_setup` builds tags correctly.
9. Create unit tests for `aider.rs` in `crates/mev-internal/src/app/cli/aider.rs`.
10. Create unit tests for `ssh.rs` in `crates/mev-internal/src/app/cli/ssh.rs`.
11. Refactor integration tests in `tests/cli/help_and_version.rs` and `tests/cli/backup.rs` to better assert behavior cleanly.
12. Refactor `TestContext` in `tests/harness/test_context.rs` to abstract I/O away from direct `std::fs` calls to boundaries.
13. Run `cargo test` to ensure all tests pass.
14. Complete pre commit steps to ensure proper testing, verification, review, and reflection are done.
