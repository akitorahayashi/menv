---
created_at: "2026-03-04"
author_role: "structural_arch"
confidence: "high"
---

## Statement

I/O Adapters are entangled with application context creation directly within CLI input contract modules, bypassing dependency injection mechanisms.

## Evidence

- path: "src/app/cli/list.rs"
  loc: "8"
  note: "`ansible_dir` is resolved directly inside the CLI `run()` method using `locator::locate_ansible_dir()?` and passed to `AppContext::new`."
- path: "src/app/cli/make.rs"
  loc: "25"
  note: "`locator::locate_ansible_dir()?` is called again in the presentation layer before creating `AppContext`."
- path: "src/app/cli/create.rs"
  loc: "30"
  note: "`locator::locate_ansible_dir()?` is called in the `create` CLI handler."
