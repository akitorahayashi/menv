---
created_at: "2024-05-15"
author_role: "data_arch"
confidence: "high"
---

## Statement

The application models a recursive directory copy function, `copy_dir_recursive`, redundantly across two different application command modules. This violates the Single Source of Truth principle by forcing future changes or bug fixes to be duplicated across boundaries without an explicit shared capability.

## Evidence

- path: "src/app/commands/deploy_configs.rs"
  loc: "line 53"
  note: "Implements `copy_dir_recursive` publicly to support the `deploy_for_tags` function."
- path: "src/app/commands/config/mod.rs"
  loc: "line 51"
  note: "Implements an almost identical private `copy_dir_recursive` function to support the `create` command."
