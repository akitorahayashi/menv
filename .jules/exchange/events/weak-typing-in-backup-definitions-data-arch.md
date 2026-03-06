---
created_at: "2024-05-15"
author_role: "data_arch"
confidence: "high"
---

## Statement

The `SettingDefinition` struct represents data types using a primitive string (`type_name: String`) rather than an explicit strong Enum type. This causes downstream formatting logic to rely on weak string matching with a silent fallback for invalid states, which is an anti-pattern that fails to encode invariants at the system boundary.

## Evidence

- path: "src/app/commands/backup/mod.rs"
  loc: "line 22"
  note: "The `SettingDefinition` model defines `type_name` as a `String`."
- path: "src/app/commands/backup/mod.rs"
  loc: "line 155"
  note: "The `format_value` function validates type identity using implicit string matching (`\"bool\"`, `\"int\"`, `\"float\"`, `\"string\"`) with a catch-all fallback `_` that masks invalid schema states."
