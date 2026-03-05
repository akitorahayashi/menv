---
label: "refacts"
---

## Goal

Remove the magic string 'list' intercept in the `backup` command positional target, structuring it as a proper CLI subcommand or option.

## Problem

The `backup` command handles the `list` (or `ls`) action through a magic string inside its positional `target` argument, rather than structuring it as a discrete subcommand or option.

## Affected Areas

### CLI and Commands

- `src/app/cli/backup.rs`
- `src/app/commands/backup/mod.rs`
- `tests/cli/backup.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- CLI regressions if the previous "list" command is still frequently used by automated scripts, or parsing errors with clap.

## Acceptance Criteria

- The `backup list` functionality is invoked explicitly (e.g., `mev backup list` or `mev backup --list`) instead of matching a magic positional string.
- Documentation is updated accordingly.

## Implementation Plan

1. In `src/app/cli/backup.rs`: Change `BackupArgs` to use a `--list` boolean flag `#[arg(short, long)] pub list: bool` and make the `target` positional argument optional `pub target: Option<String>`.
   ```rust
   #[derive(Args)]
   pub struct BackupArgs {
       #[arg(short, long, help = "List available backup targets")]
       pub list: bool,

       /// Backup target (system, vscode).
       pub target: Option<String>,
   }
   ```
2. In `src/app/cli/backup.rs`: Update the `run` function to handle the new arguments. If `args.list` is true, call a public `list_targets()` function from `commands::backup`. Otherwise, if `args.target` is Some(target), call `commands::backup::execute(&ctx, &target)`. If neither is provided, return an `AppError` indicating target is required unless `--list` is used.
3. In `src/app/commands/backup/mod.rs`: Make the existing `list_targets()` function public so it can be called from `cli/backup.rs`. Remove the magic string check `if matches!(target_input, "list" | "ls")` from the `execute` function.
4. In `tests/cli/backup.rs`: Update the CLI tests `backup_list_shows_targets` and `backup_ls_alias_shows_targets` to use `--list` instead of `list` and `ls` strings in positional arguments. Also check `backup_alias_bk_is_accepted` to use `--list`.
