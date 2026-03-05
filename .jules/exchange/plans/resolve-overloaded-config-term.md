---
label: "refacts"
---

## Goal

Disambiguate the term 'config' to clearly separate VCS user identity state from Ansible role configuration files.

## Problem

The term 'config' is currently overloaded, serving two distinct concepts: VCS user identity persistence (`MevConfig`, managed via `config set/show`) and Ansible role/application configurations deployed to local disk (`config create`). This conflation blurs the boundary between user state management and provisioned system files, leading to overloaded command namespaces and structures.

## Affected Areas

### CLI and Commands

- `src/app/cli/mod.rs`
- `src/app/cli/config.rs`
- `src/app/cli/identity.rs` (new)
- `src/app/commands/config/mod.rs`
- `src/app/commands/identity/mod.rs` (new)

### Domain and Adapters

- `src/domain/ports/config_store.rs`
- `src/domain/ports/identity_store.rs` (new)
- `src/adapters/config_store/local_json.rs`
- `src/adapters/identity_store/local_json.rs` (new)
- `src/app/context.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- UX simplicity is prioritized over excessive configuration.
- Files and classes must identify single, specific responsibilities.

## Risks

- Breaking existing user configuration paths or workflows by renaming files or commands without an alias or fallback.
- Disrupting internal tooling or dependencies that expect `mev config` to manage both concepts.
- Overlooking references to `MevConfig` in tests or other domains.

## Acceptance Criteria

- The `config` terminology is split to distinctly represent identity configuration vs role assets.
- CLI commands and directory structures clearly reflect the distinct concepts (e.g., `mev identity show/set` vs `mev config create`).
- `MevConfig` and related structures are renamed and relocated to accurately reflect their true purpose (e.g., `IdentityStore`).

## Implementation Plan

1. **Rename Domain Models**: Rename `ConfigStore` and `MevConfig` domain ports to `IdentityStore` and `IdentityState` (or similar), and move them to `src/domain/ports/identity_store.rs`.
2. **Refactor Adapters**: Move `src/adapters/config_store/local_json.rs` to `src/adapters/identity_store/local_json.rs` and update it to implement the new `IdentityStore` port. Rename the underlying file from `config.json` to `identity.json` (with a migration/fallback if necessary).
3. **Split CLI Commands**: Create `src/app/cli/identity.rs` for `show` and `set` commands. Update `src/app/cli/config.rs` to only handle the `create` (role asset deployment) command. Update `src/app/cli/mod.rs` to register the new `identity` top-level command.
4. **Split Command Handlers**: Create `src/app/commands/identity/mod.rs` and move `show` and `set` functions there. Leave `create` in `src/app/commands/config/mod.rs`.
5. **Update AppContext**: Refactor `AppContext` in `src/app/context.rs` to use `identity_store` instead of `config_store` where appropriate.
6. **Update Consumers and Tests**: Fix all call sites, tests, and mock implementations to align with the new nomenclature.
