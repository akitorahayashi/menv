---
created_at: "2024-03-04"
author_role: "rustacean"
confidence: "high"
---

## Statement

The `AnsibleAdapter` creates unnecessary clones of `.clone()` values that could either use references, or be refactored to transfer ownership or utilize more optimal borrowing. E.g., `.clone()` sprinkled to appease the borrow checker during serialization value mapping.

## Evidence

- path: "src/adapters/ansible/executor.rs"
  loc: "line 184"
  note: "`Some(serde_yaml::Value::String(s)) => vec![s.clone()]` clones the string instead of directly passing or mapping to owned if really needed, but it shows `clone()` on `s` without checking if ownership can be taken."

- path: "src/adapters/ansible/executor.rs"
  loc: "line 198"
  note: "`tag_to_role.insert(tag.clone(), name.clone());` clones tag and name inside a loop when loading catalog, when those values could probably be borrowed or ownership passed down differently."

- path: "src/adapters/ansible/executor.rs"
  loc: "line 147"
  note: "`self.tags_by_role.clone()` clone is returned in `tags_by_role()` implementation of `AnsiblePort`. The trait requires returning `HashMap<String, Vec<String>>` rather than `&HashMap<String, Vec<String>>`, forcing a heavy allocation copy."
