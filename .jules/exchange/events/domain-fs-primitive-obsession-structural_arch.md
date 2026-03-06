---
created_at: "2026-03-06"
author_role: "structural_arch"
confidence: "high"
---

## Statement

The domain layer relies heavily on stringly-typed primitives rather than strong domain concepts for arguments that represent complex behavior. For example, `tag.rs`, `ansible.rs`, and `vscode.rs` heavily pass around bare `String` and `&str` instead of wrapper types or enums. This primitive obsession means that invalid states can be represented, and validation must be continually repeated throughout the codebase rather than being enforced at the boundaries.

## Evidence


- path: "src/domain/ports/ansible.rs"
  loc: "line 10, 13, 16, 19, 22, 25"
  note: "Directly uses `&str` and `Vec<String>` to represent Ansible tags and profiles rather than strong typing, despite having dedicated concept models."
- path: "src/domain/tag.rs"
  loc: "line 46"
  note: "Returns `Vec<String>` rather than a domain-specific `Tag` collection."
- path: "src/domain/error.rs"
  loc: "line 12, 15, 18, 21, 24, 27"
  note: "Errors wrap raw Strings instead of structured error properties."
