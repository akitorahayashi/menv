---
label: "tests"
implementation_ready: false
---

## Goal

Improve test granularity, address 0% coverage gaps in critical modules, implement isolated filesystem boundaries for tests, and align the CI coverage gate with realistic metrics.

## Problem

The codebase relies heavily on slow, full-binary CLI integration tests rather than fine-grained unit behavior assertions. Standard filesystem operations rely directly on `std::fs` without mocked I/O boundaries, causing uncontrolled side effects. Furthermore, significant portions of core CLI commands (`switch`, `create`, `backup`) and external binary orchestrators (`aider.rs`, `ssh.rs`) have 0% line coverage. Finally, the CI `tarpaulin` coverage gate fails because the threshold (40%) exceeds the actual baseline (19.11%).

## Evidence

- source_event: "io-test-coverage-qa.md"
  path: "src/adapters/fs/std_fs.rs"
  loc: "Entire file"
  note: "Lacks any `#[cfg(test)]` modules or corresponding file in `tests/adapters/`. Contains pure integration wrappers that can and should be independently validated."

- source_event: "io-test-coverage-qa.md"
  path: "src/adapters/identity_store/local_json.rs"
  loc: "Entire file"
  note: "Contains logic for atomic file writes and migrations, but lacks unit tests or integration tests to verify behavior under concurrent or failure conditions."

- source_event: "io-test-coverage-qa.md"
  path: "src/app/commands/deploy_configs.rs"
  loc: "Entire file"
  note: "Performs directory deletions and recursive copying but has zero internal tests ensuring correct behavior when paths are missing, or when overwrite parameters differ."

- source_event: "test-granularity-redundancy-qa.md"
  path: "tests/cli/help_and_version.rs"
  loc: "Entire file"
  note: "Each feature/flag check spawns an entire binary via `TestContext` just to verify standard output string presence."

- source_event: "test-granularity-redundancy-qa.md"
  path: "tests/cli/backup.rs"
  loc: "backup_alias_bk_is_accepted, backup_short_list_flag_shows_targets"
  note: "Verifying single alias paths relies strictly on full binary execution testing strings rather than unit-level behavior."

- source_event: "uncontrolled-fs-deps-qa.md"
  path: "tests/harness/test_context.rs"
  loc: "std::fs::create_dir_all"
  note: "TestContext heavily relies on global standard library operations, mutating state directly to create files for testing without I/O boundaries."

- source_event: "uncontrolled-fs-deps-qa.md"
  path: "src/adapters/identity_store/local_json.rs"
  loc: "impl IdentityStore for IdentityFileStore"
  note: "Tightly coupled to `std::fs`, limiting isolation during tests as operations mutate disk directly."

- source_event: "untested-external-cli-commands-cov.md"
  path: "crates/mev-internal/src/app/cli/aider.rs"
  loc: "run_aider()"
  note: "0% tested module. It passes multiple unfiltered vectors to a command."

- source_event: "untested-external-cli-commands-cov.md"
  path: "crates/mev-internal/src/app/cli/ssh.rs"
  loc: "generate_key(), remove_host()"
  note: "0% tested logic managing ssh generation and configuration file deletion on the system disk."

- source_event: "untested-modules-coverage-risk-cov.md"
  path: "src/app/commands/switch/mod.rs"
  loc: "execute()"
  note: "This module controls identity switching logic globally using a git client, and yet records 0% coverage."

- source_event: "untested-modules-coverage-risk-cov.md"
  path: "src/app/commands/create/mod.rs"
  loc: "execute()"
  note: "Command orchestration that coordinates deploying configurations and ansible runbook steps has 0% line coverage."

- source_event: "untested-modules-coverage-risk-cov.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "execute_system(), execute_vscode(), execute()"
  note: "Backup system functionality execution functions are completely untested (0% execution module coverage)."

- source_event: "untested-modules-coverage-risk-cov.md"
  path: "src/domain/execution_plan.rs"
  loc: "ExecutionPlan::full_setup()"
  note: "Core domain function responsible for fetching FULL_SETUP_TAGS for execution setup has 0 coverage."

- source_event: "no-coverage-gate-cov.md"
  path: "coverage/cobertura.xml"
  loc: "line-rate=19.11%"
  note: "Tarpaulin execution result shows 19.11% overall line coverage, while the gate expects 40%."

- source_event: "no-coverage-gate-cov.md"
  path: "Justfile"
  loc: "coverage recipe"
  note: "Shows an unaddressed issue in repository CI gating where minimum code quality expectations are disjointed from current state."

## Change Scope

- `src/adapters/fs/`
- `src/adapters/identity_store/`
- `src/app/commands/`
- `crates/mev-internal/src/app/cli/`
- `tests/`
- `Justfile`

## Constraints

- I/O boundary components must be isolated and testable.
- Unit behavior must be asserted independently of full binary execution.
- Coverage threshold checks must align with the current baseline to avoid persistent CI failures.

## Acceptance Criteria

- Fine-grained unit tests are added for core command modules and internal external-binary orchestrators.
- Filesystem interactions in tests utilize abstract or temporary bounded mechanisms instead of relying heavily on global `std::fs`.
- The `Justfile` coverage gate is adjusted to realistically reflect current baseline expectations or the coverage is raised to meet the gate.
