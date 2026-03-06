---
created_at: "2026-03-06"
author_role: "cov"
confidence: "high"
---

## Statement

External binary executions within the `crates/mev-internal/src/app/cli/` directory such as the `aider` orchestration and `ssh` manipulation scripts have 0% testing line coverage, meaning edge cases involving malformed string arrays passing to subprocess binaries are vulnerable to breakages.

## Evidence


- path: "crates/mev-internal/src/app/cli/aider.rs"
  loc: "run_aider()"
  note: "0% tested module. It passes multiple unfiltered vectors to a command."
- path: "crates/mev-internal/src/app/cli/ssh.rs"
  loc: "generate_key(), remove_host()"
  note: "0% tested logic managing ssh generation and configuration file deletion on the system disk."
