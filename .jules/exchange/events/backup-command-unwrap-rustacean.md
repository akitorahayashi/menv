---
created_at: "2024-05-20"
author_role: "rustacean"
confidence: "high"
---

## Statement

The backup command adapter uses silent fallbacks by masking string serialization and floating point parsing errors in `src/app/commands/backup/mod.rs`. This obscures invalid state because the original value is just passed through via `unwrap_or` when `serde_json::to_string` or `f64::parse` fail.

## Evidence

- path: "src/app/commands/backup/mod.rs"
  loc: "line 169"
  note: "`serde_json::to_string(&value).unwrap_or(value)` silently ignores serialization errors."

- path: "src/app/commands/backup/mod.rs"
  loc: "line 204"
  note: "`target.parse::<f64>().map(|f| f.to_string()).unwrap_or(target)` silently ignores parsing errors."

- path: "src/app/commands/backup/mod.rs"
  loc: "line 208"
  note: "`target.parse::<f64>().map(|f| (f as i64).to_string()).unwrap_or(target)` silently ignores parsing errors."

- path: "src/app/commands/backup/mod.rs"
  loc: "line 229"
  note: "`serde_json::to_string(&value).unwrap_or(value)` silently ignores serialization errors."
