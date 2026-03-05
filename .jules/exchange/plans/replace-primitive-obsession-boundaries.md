---
label: "refacts"
---

## Goal

Eliminate primitive obsession at application boundaries by using strong Enum types instead of `&str` for domain concepts.

## Problem

The application exhibits primitive obsession at key boundaries, accepting primitive `&str` values for domain concepts like profiles and identities rather than leveraging type-safe domain models (e.g. Enums). This scatters validation logic, allows invalid states to be represented across boundaries, and obscures the Single Source of Truth for valid states.

## Affected Areas

### Domain layer
- `src/domain/profile.rs`
- `src/domain/vcs_identity.rs`
- `src/domain/execution_plan.rs`

### Application layer
- `src/app/api.rs`
- `src/app/commands/create/mod.rs`
- `src/app/commands/make/mod.rs`
- `src/app/commands/switch/mod.rs`

### CLI layer
- `src/app/cli/create.rs`
- `src/app/cli/make.rs`
- `src/app/cli/switch.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- Enumerable values and their representations must map exactly to existing identifiers for backward compatibility with CLI and Ansible.

## Risks

- Breaking the CLI parser or internal commands that currently pass `&str` for profiles.
- Regressions in Ansible execution if the enum to string conversion produces an invalid profile name.

## Acceptance Criteria

- Public API boundaries in `src/app/api.rs` accept domain Enums (`Profile`, `SwitchProfile`) rather than `&str`.
- Validation logic (`validate_machine_profile`, `validate_profile`, `resolve_switch_profile`) returns strongly typed enums.
- The `mev` tool compiles and all tests pass with the new type-safe boundary models.

## Implementation Plan

1. Define Domain Enums:
   - In `src/domain/profile.rs`, define a `Profile` enum with variants `Macbook`, `MacMini`, and `Common`. Implement `as_str` (or `Display`) to map variants back to their string representations. Update `resolve_profile`, `validate_machine_profile`, and `validate_profile` to return `Result<Profile, AppError>` or `Option<Profile>`. Update tests.
   - In `src/domain/vcs_identity.rs`, define a `SwitchProfile` enum with variants `Personal` and `Work`. Implement `as_str` or `Display`. Update `resolve_switch_profile` to return `Option<SwitchProfile>`. Update tests.
2. Update Execution Plan:
   - Modify `src/domain/execution_plan.rs` so that `ExecutionPlan` stores `Profile` rather than `String`. Update its constructors `full_setup` and `make` to accept `Profile`.
3. Update Application Commands:
   - Update `src/app/commands/create/mod.rs`, `src/app/commands/make/mod.rs`, and `src/app/commands/switch/mod.rs` to accept the new domain enums in their `execute` parameters.
   - Adjust the Ansible playbook invocations to use the string representation (`profile.as_str()`).
4. Refactor Public APIs:
   - Change `src/app/api.rs` functions (`create`, `make`, `switch`) to take the new enum types instead of `&str`. Ensure exports make these new types available to API consumers.
5. Update CLI Layer:
   - In `src/app/cli/create.rs`, `src/app/cli/make.rs`, and `src/app/cli/switch.rs`, adapt the execution to pass the strongly typed enum values derived from validation directly into the updated application commands.
6. Ensure testing, verification, review, and reflection:
   - Run tests (`cargo test`) and formatting/clippy checks. Ensure the changes compile cleanly and no warnings are introduced. Ensure proper testing, verification, review, and reflection are done.