---
created_at: "2024-05-24"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

Commands output operational logs, progress updates, and success messages to `stdout` instead of `stderr`, breaking the I/O separation contract and automation pipelines. Mixed streams break automation (e.g. piping results to jq fails if logs pollute stdout).

## Evidence

I/O contract table:
- Command: `mev create`
  - Output: Mixed progress updates and logs.
  - Exit code: 0 on success, 1 on failure.
  - Stream assignment: `stdout` via `println!` instead of `stderr`.
- Command: `mev make`
  - Output: Operational logs.
  - Exit code: 0 on success, 1 on failure.
  - Stream assignment: `stdout` via `println!` instead of `stderr`.
- Command: `mev backup`
  - Output: Operational logs.
  - Exit code: 0 on success, 1 on failure.
  - Stream assignment: `stdout` via `println!` instead of `stderr`.

Code References:
- path: "src/app/commands/create/mod.rs"
  loc: "48"
  note: "Outputs progress updates to stdout via `println!`."
- path: "src/app/commands/make/mod.rs"
  loc: "41"
  note: "Outputs operational logs to stdout via `println!`."
- path: "src/app/commands/backup/mod.rs"
  loc: "50"
  note: "Outputs operational logs to stdout via `println!`."
