---
created_at: "2024-03-06"
author_role: "qa"
confidence: "medium"
---

## Statement

Testing contracts predominantly focus on full binary CLI evaluations covering basic happy paths while under-exercising inner logic. Tests repeat binary process spawning (which is slow) to test basic flag existence. The test layer acts as an integration-heavy monolith while lacking fine-grained assertions over unit behavior.

## Evidence

- path: "tests/cli/help_and_version.rs"
  loc: "Entire file"
  note: "Each feature/flag check spawns an entire binary via `TestContext` just to verify standard output string presence."
- path: "tests/cli/backup.rs"
  loc: "backup_alias_bk_is_accepted, backup_short_list_flag_shows_targets"
  note: "Verifying single alias paths relies strictly on full binary execution testing strings rather than unit-level behavior."
