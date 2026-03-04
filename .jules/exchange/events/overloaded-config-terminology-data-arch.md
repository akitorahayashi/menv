---
created_at: "2024-05-24"
author_role: "data_arch"
confidence: "high"
---

## Statement

The concept of 'Config' is overloaded in the application, conflating VCS user identity state with Ansible role configuration files. This blurs the boundary between user state management and provisioned system files, leading to overloaded command namespaces (`mev config show/set` vs `mev config create`) and overloaded structures (`MevConfig`).

## Evidence

- path: "src/domain/ports/config_store.rs"
  loc: "line 29"
  note: "Defines `MevConfig` as a model for VCS identity configuration (`personal` and `work` identities), rather than system configuration."
- path: "src/app/commands/config/mod.rs"
  loc: "line 12, 40"
  note: "Implements `mev config show` and `mev config set` which mutate the `MevConfig` identity state."
- path: "src/app/commands/config/mod.rs"
  loc: "line 72"
  note: "Implements `mev config create` which deploys Ansible role configuration files to the local system, completely unrelated to `MevConfig` identity state."
