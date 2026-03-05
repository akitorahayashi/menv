---
label: "refacts"
implementation_ready: false
---

## Goal

Disambiguate the term 'config' which conflates VCS user identity state with Ansible role configurations.

## Problem

The concept of 'Config' is overloaded in the application, conflating VCS user identity state with Ansible role configuration files. This blurs the boundary between user state management and provisioned system files, leading to overloaded command namespaces (`mev config show/set` vs `mev config create`) and overloaded structures (`MevConfig`).

The term "config" is overloaded and serves two distinct concepts: VCS user identity persistence (`MevConfig`, managed via `config set/show`) and Ansible role/application configurations deployed to local disk (`config create`).

## Evidence

- source_event: "overloaded-config-terminology-data-arch.md"
  path: "src/domain/ports/config_store.rs"
  loc: "line 29"
  note: "Defines `MevConfig` as a model for VCS identity configuration (`personal` and `work` identities), rather than system configuration."
- source_event: "overloaded-config-terminology-data-arch.md"
  path: "src/app/commands/config/mod.rs"
  loc: "line 12, 40"
  note: "Implements `mev config show` and `mev config set` which mutate the `MevConfig` identity state."
- source_event: "overloaded-config-terminology-data-arch.md"
  path: "src/app/commands/config/mod.rs"
  loc: "line 72"
  note: "Implements `mev config create` which deploys Ansible role configuration files to the local system, completely unrelated to `MevConfig` identity state."
- source_event: "overloaded-term-config-taxonomy.md"
  path: "src/domain/ports/config_store.rs"
  loc: "line 8-10"
  note: "`MevConfig` defines VCS user identities (personal/work) persisted for Git and Jujutsu."
- source_event: "overloaded-term-config-taxonomy.md"
  path: "src/app/commands/config/mod.rs"
  loc: "line 72-111"
  note: "The `create` function inside `commands/config` deploys ansible role configuration assets (e.g., shell aliases, editor settings) to the user's local disk."
- source_event: "overloaded-term-config-taxonomy.md"
  path: "src/adapters/config_store/local_json.rs"
  loc: "line 15-20"
  note: "`config.json` stores user identity, separate from deployed role configs which are placed in role-specific subdirectories."
- source_event: "overloaded-term-config-taxonomy.md"
  path: "src/app/cli/config.rs"
  loc: "line 18-45"
  note: "CLI command bundles `show` (identity), `set` (identity), and `create` (role assets deployment) under the same parent `config` command."

## Change Scope

- `src/domain/ports/config_store.rs`
- `src/app/cli/config.rs`
- `src/app/commands/config/mod.rs`
- `src/adapters/config_store/local_json.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- The `config` terminology is split to distinctly represent identity configuration vs role assets.
- CLI commands and directory structures clearly reflect the distinct concepts.
