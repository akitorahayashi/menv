---
created_at: "2026-03-04"
author_role: "taxonomy"
confidence: "high"
---

## Statement

The term "config" is overloaded and serves two distinct concepts: VCS user identity persistence (`MevConfig`, managed via `config set/show`) and Ansible role/application configurations deployed to local disk (`config create`).

## Evidence

- path: "src/domain/ports/config_store.rs"
  loc: "line 8-10"
  note: "`MevConfig` defines VCS user identities (personal/work) persisted for Git and Jujutsu."
- path: "src/app/commands/config/mod.rs"
  loc: "line 72-111"
  note: "The `create` function inside `commands/config` deploys ansible role configuration assets (e.g., shell aliases, editor settings) to the user's local disk."
- path: "src/adapters/config_store/local_json.rs"
  loc: "line 15-20"
  note: "`config.json` stores user identity, separate from deployed role configs which are placed in role-specific subdirectories."
- path: "src/app/cli/config.rs"
  loc: "line 18-45"
  note: "CLI command bundles `show` (identity), `set` (identity), and `create` (role assets deployment) under the same parent `config` command."
