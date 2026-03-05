---
label: "refacts"
---

## Goal

Rename generic `AppContext` to distinctly describe its domain responsibility, removing ambiguous naming.

## Problem

The codebase uses vague names like `AppContext` which violates the principle that names must not hide responsibility or be ambiguous. Using generic wrappers like `AppContext` without distinct domain nouns makes discovery harder.

## Affected Areas

### `src/app/`

- `src/app/context.rs`
- `src/app/mod.rs`
- `src/app/api.rs`
- `src/app/commands/list/mod.rs`
- `src/app/commands/config/mod.rs`
- `src/app/commands/switch/mod.rs`
- `src/app/commands/make/mod.rs`
- `src/app/commands/backup/mod.rs`
- `src/app/commands/create/mod.rs`
- `src/app/cli/config.rs`
- `src/app/cli/backup.rs`
- `src/app/cli/update.rs`
- `src/app/cli/create.rs`
- `src/app/cli/make.rs`
- `src/app/cli/switch.rs`
- `src/app/cli/list.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- Widespread refactoring of a core dependency container might cause compilation errors if a reference is missed.

## Acceptance Criteria

- The `AppContext` structure is renamed to something specific, like `DependencyContainer` or a context specific to its usage.
- All references in `src/app/context.rs` and dependent modules are updated.

## Implementation Plan

1. Rename `AppContext` to `DependencyContainer` in `src/app/context.rs`.
2. Update all usages of `AppContext` to `DependencyContainer` throughout the `src/app` directory.
3. Verify that all changes compile by running `cargo check`.
