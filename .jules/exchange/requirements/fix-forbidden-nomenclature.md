---
label: "refacts"
implementation_ready: false
---

## Goal

Remove explicitly forbidden and ambiguous names like `core` and `helpers` from directory names, module documentation, and replace the term `Profile` when referring to VCS user identities.

## Problem

The repository's AGENTS.md strictly forbids using ambiguous names such as `core/`, `utils/`, and `helpers/`. These terms are currently used in an Ansible role directory and in several CLI module documentation comments. Additionally, the term "Profile" is used incorrectly in the `mev identity show` CLI output to refer to VCS user identities, when it should strictly refer to machine hardware configurations.

## Evidence

- source_event: "core-directory-forbidden-taxonomy.md"
  path: "dist/mev/ansible/roles/shell/config/common/alias/core"
  loc: "directory path"
  note: "Uses the forbidden ambiguous name 'core'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "src/app/cli/mod.rs"
  loc: "67, 71, 79"
  note: "Doc comments use the ambiguous and forbidden term 'helpers'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "274"
  note: "Comment uses the term 'Shared helpers'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "crates/mev-internal/src/app/cli/mod.rs"
  loc: "23, 27, 35"
  note: "Doc comments use the term 'helpers' and 'helper'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "crates/mev-internal/src/app/cli/aider.rs"
  loc: "1"
  note: "Module doc comment uses 'helpers'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "crates/mev-internal/src/app/cli/shell.rs"
  loc: "1"
  note: "Module doc comment uses 'helper'."

- source_event: "helpers-usage-forbidden-taxonomy.md"
  path: "crates/mev-internal/src/app/cli/vcs.rs"
  loc: "1"
  note: "Module doc comment uses 'helpers'."

- source_event: "profile-identity-collision-taxonomy.md"
  path: "src/app/commands/identity/mod.rs"
  loc: "23"
  note: "Uses the word 'Profile' to label 'personal' and 'work' identities, contradicting domain definitions."

## Change Scope

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

## Acceptance Criteria

- The `core` directory in `dist/mev/ansible/roles/shell/config/common/alias/` is renamed to a specific responsibility.
- The terms `helper` and `helpers` are removed from the specified doc comments.
- The CLI output in `src/app/commands/identity/mod.rs` uses "Identity" or similar instead of "Profile".
