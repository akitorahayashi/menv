---
label: "refacts"
---

## Goal

Remove explicitly forbidden and ambiguous names like `core` and `helpers` from directory names, module documentation, and replace the term `Profile` when referring to VCS user identities.

## Problem

The repository's AGENTS.md strictly forbids using ambiguous names such as `core/`, `utils/`, and `helpers/`. These terms are currently used in an Ansible role directory and in several CLI module documentation comments. Additionally, the term "Profile" is used incorrectly in the `mev identity show` CLI output to refer to VCS user identities, when it should strictly refer to machine hardware configurations.

## Affected Areas

### Taxonomy & Nomenclature

- `dist/mev/ansible/roles/shell/config/common/alias/core`
- `src/app/cli/mod.rs`
- `src/app/commands/backup/mod.rs`
- `crates/mev-internal/src/app/cli/mod.rs`
- `crates/mev-internal/src/app/cli/aider.rs`
- `crates/mev-internal/src/app/cli/shell.rs`
- `crates/mev-internal/src/app/cli/vcs.rs`
- `src/app/commands/identity/mod.rs`

## Constraints

- Ambiguous names like `core`, `utils`, `helpers` must not be used.
- Renaming, deleting, or restructuring code must be followed by a comprehensive search for old terms.
- The term 'profile' is strictly reserved for machine hardware configurations.

## Risks

- Renaming the Ansible directory might require updating references in playbook or configuration loading code (though a prior search indicated no references to `alias/core`).
- Updating CLI output for `mev identity show` might break existing tests parsing that output.

## Acceptance Criteria

- The `core` directory in `dist/mev/ansible/roles/shell/config/common/alias/` is renamed to a specific responsibility (e.g., `system` or `os`).
- The terms `helper` and `helpers` are removed from the specified doc comments.
- The CLI output in `src/app/commands/identity/mod.rs` uses "Identity" or similar instead of "Profile".

## Implementation Plan

1. Rename the directory `dist/mev/ansible/roles/shell/config/common/alias/core` to `dist/mev/ansible/roles/shell/config/common/alias/system`.
2. Remove the terms `helper` and `helpers` from the documentation comments in `src/app/cli/mod.rs`, `src/app/commands/backup/mod.rs`, `crates/mev-internal/src/app/cli/mod.rs`, `crates/mev-internal/src/app/cli/aider.rs`, `crates/mev-internal/src/app/cli/shell.rs`, and `crates/mev-internal/src/app/cli/vcs.rs`.
3. Change the header from "Profile" to "Identity" in `src/app/commands/identity/mod.rs`.
4. Run the test suite (`cargo test`) to ensure no regressions were introduced.
