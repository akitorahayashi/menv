---
created_at: "2024-05-24"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

The `backup` command uses a `--list` flag as an action, substituting the required `target` object, indicating structural drift from the standard `verb [object]` form.

## Evidence

- path: "src/app/cli/backup.rs"
  loc: "12"
  note: "The `--list` flag acts as an alternative execution path, rendering the `target` argument optional."
- path: "src/app/commands/backup/mod.rs"
  loc: "302"
  note: "The `list_targets` function is invoked by the `--list` flag instead of having a dedicated `list` object or subcommand."
