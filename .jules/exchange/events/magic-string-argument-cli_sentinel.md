---
created_at: "2026-03-04"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

The `backup` command handles the `list` (or `ls`) action through a magic string inside its positional `target` argument, rather than structuring it as a discrete subcommand or option.

## Evidence

- path: "src/app/commands/backup/mod.rs"
  loc: "35-38"
  note: "Intercepts the string 'list' or 'ls' within the positional `target_input` argument to execute the `list_targets()` function instead of processing a valid backup target, overloading the argument's semantics and violating the 'verb [object]' structure."
- path: "src/app/cli/backup.rs"
  loc: "12-14"
  note: "The help text documents that the `target` argument can accept 'list' as a special value, confirming the structural drift away from a dedicated `list` subcommand."
