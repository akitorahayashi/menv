---
label: "bugs"
implementation_ready: false
---

## Goal

Ensure CLI commands follow structural consistency, enforce explicit safety contracts for destructive operations, and properly separate I/O streams for automation.

## Problem

The CLI layer suffers from structural drift, inconsistent safety, and I/O pollution. The `backup` command substitutes its required target object with a `--list` action flag, drifting from standard verb-object form. The `backup` command also lacks an `--overwrite` flag for destructive file-writing operations, unlike `create` and `make`. Finally, commands like `create`, `make`, and `backup` output operational logs and progress updates to `stdout` instead of `stderr`, breaking automation pipelines.

## Evidence

- source_event: "inconsistent-destructive-safety-backup-cli-sentinel.md"
  path: "src/app/cli/backup.rs"
  loc: "11-17"
  note: "Lacks an `--overwrite` flag or confirmation prompt for file-writing operations."

- source_event: "inconsistent-destructive-safety-backup-cli-sentinel.md"
  path: "src/app/cli/create.rs"
  loc: "18"
  note: "The `CreateArgs` struct defines an `--overwrite` flag, demonstrating established safety contracts."

- source_event: "inconsistent-destructive-safety-backup-cli-sentinel.md"
  path: "src/app/cli/make.rs"
  loc: "22"
  note: "The `MakeArgs` struct defines an `--overwrite` flag, further establishing the safety contract."

- source_event: "mixed-io-stdout-pollution-cli-sentinel.md"
  path: "src/app/commands/create/mod.rs"
  loc: "48"
  note: "Outputs progress updates to stdout via `println!` instead of `stderr`."

- source_event: "mixed-io-stdout-pollution-cli-sentinel.md"
  path: "src/app/commands/make/mod.rs"
  loc: "41"
  note: "Outputs operational logs to stdout via `println!` instead of `stderr`."

- source_event: "mixed-io-stdout-pollution-cli-sentinel.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "50"
  note: "Outputs operational logs to stdout via `println!` instead of `stderr`."

- source_event: "structural-drift-backup-list-cli-sentinel.md"
  path: "src/app/cli/backup.rs"
  loc: "12"
  note: "The `--list` flag acts as an alternative execution path, rendering the `target` argument optional."

- source_event: "structural-drift-backup-list-cli-sentinel.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "302"
  note: "The `list_targets` function is invoked by the `--list` flag instead of having a dedicated `list` object or subcommand."


## Change Scope

- `src/app/cli/backup.rs`
- `src/app/commands/backup/mod.rs`
- `src/app/commands/create/mod.rs`
- `src/app/commands/make/mod.rs`

## Constraints

- Structural consistency (verb-object form) must be maintained.
- Destructive operations require explicit confirmation or `--overwrite` flags.
- Operational logs must be output to `stderr` to avoid polluting `stdout`.

## Acceptance Criteria

- The `backup` command implements a dedicated `list` subcommand or explicitly handles targets without substituting them with a flag.
- The `backup` command includes an `--overwrite` flag for file writes.
- `create`, `make`, and `backup` commands use `eprintln!` or a proper logging mechanism to write operational logs to `stderr`.
