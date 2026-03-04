---
created_at: "2024-03-04"
author_role: "rustacean"
confidence: "high"
---

## Statement

The CLI commands in `mev-internal` use `unwrap()` and `expect()` directly, especially around JSON parsing and filesystem operations, bypassing proper error handling and propagation which violates the principle of "errors are part of the contract".

## Evidence

- path: "crates/mev-internal/src/app/cli/shell.rs"
  loc: "line 85"
  note: "`output_path.file_name().unwrap().to_string_lossy()` assumes the output path will always have a valid file name which could panic."

- path: "crates/mev-internal/src/app/cli/ssh.rs"
  loc: "line 265, 267"
  note: "Using `unwrap()` on `tempfile::tempdir()` and `collect_hosts` in tests hides failure modes instead of using proper `Result` propagation or more explicit assertions."

- path: "src/domain/profile.rs"
  loc: "line 82, 83"
  note: "Tests in domain profile contain multiple `unwrap()` usages directly."