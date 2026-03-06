---
created_at: "2024-05-24"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

Commands output operational logs, progress updates, and success messages to `stdout` instead of `stderr`, breaking the I/O separation contract and automation pipelines.

## Evidence

- path: "src/app/commands/create/mod.rs"
  loc: "48"
  note: "Outputs progress updates to stdout via `println!`."
- path: "src/app/commands/make/mod.rs"
  loc: "41"
  note: "Outputs operational logs to stdout via `println!`."
- path: "src/app/commands/backup/mod.rs"
  loc: "50"
  note: "Outputs operational logs to stdout via `println!`."
