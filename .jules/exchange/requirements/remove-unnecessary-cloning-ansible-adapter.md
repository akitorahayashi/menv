---
label: "refacts"
implementation_ready: false
---

## Goal

Optimize the `AnsibleAdapter` by removing unnecessary `.clone()` calls and utilizing better borrowing or ownership transfer.

## Problem

The `AnsibleAdapter` creates unnecessary clones of `.clone()` values that could either use references, or be refactored to transfer ownership or utilize more optimal borrowing. E.g., `.clone()` sprinkled to appease the borrow checker during serialization value mapping.

## Evidence

- source_event: "unnecessary-cloning-in-ansible-adapter-rustacean.md"
  path: "src/adapters/ansible/executor.rs"
  loc: "line 184"
  note: "`Some(serde_yaml::Value::String(s)) => vec![s.clone()]` clones the string instead of directly passing or mapping to owned if really needed, but it shows `clone()` on `s` without checking if ownership can be taken."
- source_event: "unnecessary-cloning-in-ansible-adapter-rustacean.md"
  path: "src/adapters/ansible/executor.rs"
  loc: "line 198"
  note: "`tag_to_role.insert(tag.clone(), name.clone());` clones tag and name inside a loop when loading catalog, when those values could probably be borrowed or ownership passed down differently."
- source_event: "unnecessary-cloning-in-ansible-adapter-rustacean.md"
  path: "src/adapters/ansible/executor.rs"
  loc: "line 147"
  note: "`self.tags_by_role.clone()` clone is returned in `tags_by_role()` implementation of `AnsiblePort`. The trait requires returning `HashMap<String, Vec<String>>` rather than `&HashMap<String, Vec<String>>`, forcing a heavy allocation copy."

## Change Scope

- `src/adapters/ansible/executor.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- `AnsibleAdapter` serialization value mapping and tag insertion logic avoid redundant clones.
- The `AnsiblePort` trait definition is updated if necessary to avoid heavy allocation copies.
