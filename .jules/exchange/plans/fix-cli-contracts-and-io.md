---
label: "bugs"
---

## Goal
Ensure CLI commands follow structural consistency, enforce explicit safety contracts for destructive operations, and properly separate I/O streams for automation.

## Problem
The CLI layer suffers from structural drift, inconsistent safety, and I/O pollution. The `backup` command substitutes its required target object with a `--list` action flag, drifting from standard verb-object form. The `backup` command also lacks an `--overwrite` flag for destructive file-writing operations, unlike `create` and `make`. Finally, commands like `create`, `make`, and `backup` output operational logs and progress updates to `stdout` instead of `stderr`, breaking automation pipelines.

## Affected Areas
### src/app/cli/backup.rs
- Needs refactoring to match standard verb-object form or at least change `--list` to not act as an action flag on the same level as a required positional argument, OR refactor to `BackupArgs` with a subcommand.
- Needs an `--overwrite` flag.

### src/app/commands/backup/mod.rs
- Needs to handle the `--overwrite` flag and refuse to overwrite existing files unless the flag is passed.
- Needs to change `println!` to `eprintln!` for operational logs.

### src/app/commands/create/mod.rs
- Needs to change `println!` to `eprintln!` for operational logs.

### src/app/commands/make/mod.rs
- Needs to change `println!` to `eprintln!` for operational logs.

## Constraints
- Structural consistency (verb-object form) must be maintained.
- Destructive operations require explicit confirmation or `--overwrite` flags.
- Operational logs must be output to `stderr` to avoid polluting `stdout`.

## Risks
- Breaking existing automation scripts that rely on the old output format.
- Potential loss of data if `--overwrite` is misused or implemented incorrectly.

## Acceptance Criteria
- The `backup` command implements a dedicated `list` subcommand or explicitly handles targets without substituting them with a flag.
- The `backup` command includes an `--overwrite` flag for file writes.
- `create`, `make`, and `backup` commands use `eprintln!` or a proper logging mechanism to write operational logs to `stderr`.

## Implementation Plan
1. Refactor `BackupArgs` in `src/app/cli/backup.rs` to use subcommands (`List` and `Target`).
2. Add an `--overwrite` flag to `Target` subcommand in `BackupArgs`.
3. Update `src/app/commands/backup/mod.rs` to handle `--overwrite` and use `eprintln!`.
4. Update `src/app/commands/create/mod.rs` and `src/app/commands/make/mod.rs` to use `eprintln!`.
5. Run tests.