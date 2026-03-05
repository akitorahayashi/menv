---
label: "refacts"
implementation_ready: false
---

## Goal

Remove the magic string 'list' intercept in the `backup` command positional target, structuring it as a proper CLI subcommand or option.

## Problem

The `backup` command handles the `list` (or `ls`) action through a magic string inside its positional `target` argument, rather than structuring it as a discrete subcommand or option.

## Evidence

- source_event: "magic-string-argument-cli-sentinel.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "35-38"
  note: "Intercepts the string 'list' or 'ls' within the positional `target_input` argument to execute the `list_targets()` function instead of processing a valid backup target, overloading the argument's semantics and violating the 'verb [object]' structure."
- source_event: "magic-string-argument-cli-sentinel.md"
  path: "src/app/cli/backup.rs"
  loc: "12-14"
  note: "The help text documents that the `target` argument can accept 'list' as a special value, confirming the structural drift away from a dedicated `list` subcommand."

## Change Scope

- `src/app/cli/backup.rs`
- `src/app/commands/backup/mod.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- The `backup list` functionality is invoked explicitly (e.g., `mev backup list` or `mev backup --list`) instead of matching a magic positional string.
- Documentation is updated accordingly.
