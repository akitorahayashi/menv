---
label: "tests"
---

## Goal

Improve code coverage for critical paths including I/O adapters, system backups, configuration commands, and CLI execution paths.

## Problem

The application has a clear boundary design between pure logic and side effects, but it is lacking unit tests for many of the I/O adapters, meaning that the integration points with the OS and external binaries are relatively untested. Additionally, some tests directly use system commands without dependency injection. Overall line coverage is critically low at 18.39%, representing a significant regression risk for unverified paths that orchestrate complex domain actions and interface directly with external state and user configurations.

## Affected Areas

### CLI and Commands

- `src/app/cli/`
- `src/app/commands/`
- `src/app/api.rs`

### Domain

- `src/domain/execution_plan.rs`

### Adapters

- `src/adapters/`
- `src/adapters/macos_defaults/cli.rs`
- `src/adapters/version_source/pipx.rs`

## Constraints

- Feature additions and refactorings include the removal of old modules and deprecated features to eliminate technical debt, bugs, and complexity.
- Class and file must not have ambiguous names or responsibilities such as base, common, core, utils, or helpers.
- Systemic fixes are preferred over patches; invariants and owning components are addressed at boundaries to benefit all call sites without workarounds.

## Risks

- Lacking tests for adapters risks silent IO failures or corrupted config parsing.
- Missing coverage for CLI models and parsing logic creates risks of parsing errors or misconfigured user inputs crashing the application.

## Acceptance Criteria

- Unit or integration tests are added for the filesystem adapter, config store json parsing, and macOS defaults CLI.
- CLI models and parsing logic have foundational test coverage.

## Implementation Plan

1. Inject adapter traits and write unit tests for `MacosDefaultsCli` in `src/adapters/macos_defaults/cli.rs`.
2. Refactor `PipxVersionSource` in `src/adapters/version_source/pipx.rs` to use injected dependencies and add unit tests.
3. Write unit tests for `ExecutionPlan` in `src/domain/execution_plan.rs` to verify `full_setup` and `make` behavior.
4. Add tests for CLI models and parsing logic in `src/app/cli/`.
5. Implement tests for critical state transitions and commands (`create`, `list`, `make`, `deploy_configs`, `backup`, `config`) in `src/app/commands/`.
6. Add unit tests for the API application layer orchestrator in `src/app/api.rs`.
7. Write tests for key system integration layers like the filesystem adapter (`src/adapters/std_fs.rs`), config store json parsing, and vscode CLI.
