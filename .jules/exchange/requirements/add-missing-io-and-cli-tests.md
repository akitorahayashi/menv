---
label: "tests"
implementation_ready: false
---

## Goal

Improve code coverage for critical paths including I/O adapters, system backups, configuration commands, and CLI execution paths.

## Problem

The application has a clear boundary design between pure logic and side effects, but it is lacking unit tests for many of the I/O adapters, meaning that the integration points with the OS and external binaries are relatively untested. Additionally, some tests directly use system commands without dependency injection.

Based on the `cargo tarpaulin` line coverage report (`just coverage`), critical domains such as Ansible execution paths, filesystem adapters, system backups, configuration creation, list commands, make commands, and app CLI execution are almost entirely uncovered. Overall line coverage is critically low at 18.39%. This represents a significant regression risk, particularly because these unverified paths orchestrate complex domain actions and interface directly with external state and user configurations.

## Evidence

- source_event: "io-boundaries-qa.md"
  path: "src/adapters/macos_defaults/cli.rs"
  loc: "line 17"
  note: "MacosDefaultsCli adapter uses Command::new(\"defaults\") directly without an adapter trait, making it hard to test."
- source_event: "io-boundaries-qa.md"
  path: "src/adapters/version_source/pipx.rs"
  loc: "line 22"
  note: "PipxVersionSource uses Command::new(\"pipx\") directly, tightly coupling the test to the local pipx installation."
- source_event: "io-boundaries-qa.md"
  path: "src/domain/execution_plan.rs"
  loc: "line 11"
  note: "ExecutionPlan is pure logic, completely isolated from side effects, which is a good pattern, but it lacks dedicated unit tests to verify full_setup and make behavior."
- source_event: "untested-cli-adapters-and-commands-cov.md"
  path: "src/app/cli/"
  loc: "0/313 lines"
  note: "CLI models and parsing logic (aider, shell, ssh, vcs, mod) lack line coverage entirely, creating risks of parsing errors or misconfigured user inputs crashing the application."
- source_event: "untested-cli-adapters-and-commands-cov.md"
  path: "src/app/commands"
  loc: "31/393 lines"
  note: "Critical state transitions and user workflows like `create`, `list`, `make`, `deploy_configs`, and parts of `backup` and `config` are missing or have extremely low line coverage, jeopardizing system provisioning and orchestration safety."
- source_event: "untested-cli-adapters-and-commands-cov.md"
  path: "src/app/api.rs"
  loc: "0/34 lines"
  note: "The API application layer orchestrator has zero line coverage, meaning the primary entry point linking domain models to adapter operations is unverified."
- source_event: "untested-cli-adapters-and-commands-cov.md"
  path: "src/adapters"
  loc: "64/262 lines"
  note: "Key system integration layers, including the filesystem (`std_fs.rs`), vscode CLI, config store json parsing, and macos defaults CLI, are entirely untested or have low line coverage. Because adapters mutate system state and read files, lacking tests here risks silent IO failures or corrupted config parsing."

## Change Scope

- `src/app/commands`
- `src/app/api.rs`
- `src/domain/execution_plan.rs`
- `src/app/cli/`
- `src/adapters/version_source/pipx.rs`
- `src/adapters`
- `src/adapters/macos_defaults/cli.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- Unit or integration tests are added for the filesystem adapter, config store json parsing, and macOS defaults CLI.
- CLI models and parsing logic have foundational test coverage.
