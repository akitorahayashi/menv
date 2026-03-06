---
created_at: "2024-05-24"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

The `backup` command lacks an `--overwrite` flag or confirmation prompt, making its file-writing operations potentially unsafe compared to commands like `create` and `make`.

## Evidence

Destructive operation specs:
- Confirmation path: None (silently overwrites).
- Dry-run behavior: None supported.
- Exit codes: 0 on success, 1 on failure.

Code References:
- path: "src/app/cli/backup.rs"
  loc: "11-17"
  note: "The `BackupArgs` struct does not define an `--overwrite` flag or any other safety mechanism."
- path: "src/app/cli/create.rs"
  loc: "18"
  note: "The `CreateArgs` struct defines an `--overwrite` flag, demonstrating established safety contracts."
- path: "src/app/cli/make.rs"
  loc: "22"
  note: "The `MakeArgs` struct defines an `--overwrite` flag, further establishing the safety contract."
