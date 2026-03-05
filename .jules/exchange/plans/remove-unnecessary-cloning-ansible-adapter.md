---
label: "refacts"
---

## Goal

Optimize the `AnsibleAdapter` by removing unnecessary `.clone()` calls and utilizing better borrowing or ownership transfer.

## Problem

The `AnsibleAdapter` creates unnecessary clones of values that could either use references, or be refactored to transfer ownership or utilize more optimal borrowing. For example, `.clone()` is sprinkled to appease the borrow checker during serialization value mapping.

## Affected Areas

### Ansible Adapter and Port

- `src/adapters/ansible/executor.rs`
- `src/domain/ports/ansible.rs`
- `src/app/commands/list/mod.rs` (if affected by port trait change)

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- The `AnsiblePort` trait definition needs to be updated if necessary to avoid heavy allocation copies.

## Risks

- Changing trait definitions (`AnsiblePort::tags_by_role`) might require updates in multiple calling locations (e.g., `src/app/commands/list/mod.rs`).
- Borrow checker issues might arise if references outlive the struct, so proper lifetime annotations might be needed if returning references.

## Acceptance Criteria

- `AnsibleAdapter` serialization value mapping and tag insertion logic avoid redundant clones.
- The `AnsiblePort` trait definition is updated to return references rather than cloned owned values where applicable, avoiding heavy allocation copies.
- `cargo test` and `cargo check` pass with all changes.

## Implementation Plan

1. In `src/domain/ports/ansible.rs`, update `AnsiblePort::tags_by_role(&self)` to return `&HashMap<String, Vec<String>>` instead of `HashMap<String, Vec<String>>`.
2. In `src/adapters/ansible/executor.rs`, update the `tags_by_role` method implementation to return `&self.tags_by_role` without cloning.
3. Update `src/app/commands/list/mod.rs` line 11 (or around there) where `ctx.ansible.tags_by_role()` is called to handle borrowing instead of taking ownership, if necessary.
4. In `src/adapters/ansible/executor.rs` line 184, change `Some(serde_yaml::Value::String(s)) => vec![s.clone()],` to `Some(serde_yaml::Value::String(s)) => vec![s.to_string()],` or transfer ownership if possible.
5. In `src/adapters/ansible/executor.rs` line 198, inside `load_catalog`, `tag_to_role.insert(tag.clone(), name.clone());` should be optimized. `name` can be cloned once per role instead of per tag, or passed via reference if applicable.
6. Run `cargo test` and `cargo check` to ensure the project still compiles and tests pass.
