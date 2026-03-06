---
label: "refacts"
---

## Goal

Replace primitive string types with strong domain concepts (wrapper types or enums) at domain boundaries.

## Problem

The domain layer and data definitions rely heavily on stringly-typed primitives (`String` and `&str`) instead of strong types. This allows invalid states to be represented and forces validation to be repeated, rather than enforcing it at boundaries. For example, Ansible tags and profiles are passed as strings, and errors wrap raw strings. Similarly, backup setting definitions use weak strings to represent data types.

## Affected Areas

### Domain Boundary & Ansible Port

- `src/domain/ports/ansible.rs`
- `src/domain/tag.rs`
- `src/domain/error.rs`
- `src/domain/execution_plan.rs`
- `src/adapters/ansible/executor.rs`

### Commands

- `src/app/commands/backup/mod.rs`
- `src/app/commands/create/mod.rs`
- `src/app/commands/make/mod.rs`
- `src/app/commands/deploy_configs.rs`

## Constraints

- Application boundaries and public APIs use strong Enum types rather than primitive `&str` values.
- Systemic fixes are preferred over patches; invariants must be addressed at boundaries.

## Risks

- The new `SettingType` enum should use an `Other(String)` variant or similar fallback if needed to prevent breaking changes.
- Updating `AnsiblePort` will break implementation in `AnsibleAdapter`. The adapter needs to be updated synchronously, and all caller commands must be updated to use the strong types.

## Acceptance Criteria

- `src/domain/ports/ansible.rs` uses strong domain types (`Profile` enum, `Tag` wrapper) instead of `String` or `Vec<String>`.
- `src/domain/tag.rs` introduces a `Tag` wrapper and `resolve_tags` returns `Vec<Tag>`.
- `src/domain/error.rs` errors use structured properties instead of wrapping raw strings.
- `SettingDefinition` in `src/app/commands/backup/mod.rs` uses a strong Enum type for `type_name`.

## Implementation Plan

1. **Introduce `Tag` wrapper in `src/domain/tag.rs`**
   - Define a strong `Tag` type wrapper: `#[derive(Debug, Clone, PartialEq, Eq, Hash)] pub struct Tag(pub String);`
   - Update `resolve_tags` to return `Vec<Tag>`.
   - Update `FULL_SETUP_TAGS` handling or types to align with `Tag`.
   - Implement `std::fmt::Display` for `Tag`.
2. **Refactor `AppError` in `src/domain/error.rs`**
   - Convert tuple variants (`InvalidProfile(String)`, `InvalidIdentity(String)`, `InvalidTag(String)`, `Config(String)`, `Update(String)`, and `Backup(String)`) to struct variants with a named property like `{ message: String }` or `{ input: String }`.
   - Update `std::fmt::Display` to match the new struct variants.
3. **Update `AnsiblePort` interface in `src/domain/ports/ansible.rs`**
   - Replace `profile: &str` with `profile: &crate::domain::profile::Profile` in `run_playbook`.
   - Replace `tags: &[String]` with `tags: &[crate::domain::tag::Tag]` in `run_playbook`.
   - Replace `tags: &[String]` with `tags: &[crate::domain::tag::Tag]` in `validate_tags`.
   - Update `all_tags`, `tags_by_role`, and `role_for_tag` to use `crate::domain::tag::Tag` instead of `String` where applicable.
4. **Update `AnsibleAdapter` in `src/adapters/ansible/executor.rs`**
   - Update `AnsibleAdapter`'s implementation of `AnsiblePort` to use `Profile` and `Tag`.
   - Update `run_playbook` signature and convert `Tag` values via `.0` (or display) when invoking `ansible-playbook`.
   - Update `validate_tags`, `all_tags`, and other trait methods. Adjust internal map lookups as needed.
5. **Update `ExecutionPlan` in `src/domain/execution_plan.rs`**
   - Change the `tags` field in `ExecutionPlan` to `Vec<crate::domain::tag::Tag>`.
   - Update `ExecutionPlan::full_setup` and `ExecutionPlan::make` to map strings to `Tag` objects.
6. **Update Commands**
   - In `src/app/commands/create/mod.rs`, update usage of `ctx.ansible.all_tags()` and `FULL_SETUP_TAGS` to use `Tag`. Update the loop running playbook with `Tag` slices.
   - In `src/app/commands/make/mod.rs`, update logic resolving strings to `Tag` objects.
   - In `src/app/commands/deploy_configs.rs`, update `deploy_for_tags` signature from `tags: &[String]` to `tags: &[crate::domain::tag::Tag]`.
7. **Refactor `SettingDefinition` in `src/app/commands/backup/mod.rs`**
   - Define a `SettingType` enum with variants `Bool`, `Int`, `Float`, `String`, and an untagged custom fallback `Other(String)` for robust deserialization.
   - Update `SettingDefinition.type_name` to be of type `SettingType`.
   - Update formatting and evaluation logic to match on the `SettingType` enum instead of string matching.
8. **Fix compilation errors**
   - Use `cargo check` and `cargo test` iteratively to find and fix all type mismatches caused by the new structured properties and wrappers. Check any untested adapter code.
