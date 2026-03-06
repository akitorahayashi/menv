---
label: "refacts"
implementation_ready: false
---

## Goal

Replace primitive string types with strong domain concepts (wrapper types or enums) at domain boundaries.

## Problem

The domain layer and data definitions rely heavily on stringly-typed primitives (`String` and `&str`) instead of strong types. This allows invalid states to be represented and forces validation to be repeated, rather than enforcing it at boundaries. For example, Ansible tags and profiles are passed as strings, and errors wrap raw strings. Similarly, backup setting definitions use weak strings to represent data types.

## Evidence

- source_event: "domain-fs-primitive-obsession-structural-arch.md"
  path: "src/domain/ports/ansible.rs"
  loc: "line 10, 13, 16, 19, 22, 25"
  note: "Directly uses `&str` and `Vec<String>` to represent domain concepts like tags, profiles, and errors."

- source_event: "domain-fs-primitive-obsession-structural-arch.md"
  path: "src/domain/tag.rs"
  loc: "line 46"
  note: "Returns `Vec<String>` rather than a domain-specific `Tag` collection."

- source_event: "domain-fs-primitive-obsession-structural-arch.md"
  path: "src/domain/error.rs"
  loc: "line 12, 15, 18, 21, 24, 27"
  note: "Errors wrap raw Strings instead of structured error properties."

- source_event: "weak-typing-in-backup-definitions-data-arch.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "line 22"
  note: "The `SettingDefinition` model defines `type_name` as a `String`."

- source_event: "weak-typing-in-backup-definitions-data-arch.md"
  path: "src/app/commands/backup/mod.rs"
  loc: "line 155"
  note: "The `format_value` function validates type identity using implicit string matching."

## Change Scope

- `src/domain/ports/ansible.rs`
- `src/domain/tag.rs`
- `src/domain/error.rs`
- `src/app/commands/backup/mod.rs`

## Constraints

- Application boundaries and public APIs use strong Enum types rather than primitive `&str` values.
- Systemic fixes are preferred over patches; invariants must be addressed at boundaries.

## Acceptance Criteria

- `src/domain/ports/ansible.rs` and `src/domain/tag.rs` use strong domain types (e.g., a `Tag` collection, `Profile` enum) instead of `String` or `Vec<String>`.
- `src/domain/error.rs` errors use structured properties instead of wrapping raw strings.
- `SettingDefinition` in `src/app/commands/backup/mod.rs` uses a strong Enum type for `type_name`.
