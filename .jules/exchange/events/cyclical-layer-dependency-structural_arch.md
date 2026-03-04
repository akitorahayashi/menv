---
created_at: "2026-03-04"
author_role: "structural_arch"
confidence: "high"
---

## Statement

Presentation logic (CLI routing) and App/Domain orchestration logic are tightly coupled and duplicate initialization logic, specifically `AnsibleLocator` inside both `cli` and `api` modules.

## Evidence

- path: "src/app/api.rs"
  loc: "7-8"
  note: "The API module depends on `crate::adapters::ansible::locator`, effectively entangling the public API with the implementation detail of how Ansible directories are discovered."
- path: "src/app/cli/config.rs"
  loc: "5"
  note: "Like other CLI modules, the `config` CLI handler duplicates `locator::locate_ansible_dir()?`."
- path: "src/app/context.rs"
  loc: "8-16"
  note: "`AppContext` knows about concrete adapters (e.g. `AnsibleAdapter`, `ConfigFileStore`, `StdFs`), preventing true dependency inversion where `AppContext` should only depend on port interfaces."
