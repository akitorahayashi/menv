---
created_at: "2025-03-05"
author_role: "qa"
confidence: "high"
---

## Statement

The CLI tests are tightly coupled to the system state via `harness::TestContext`, which uses actual commands like `cli().assert().success()` without isolated seams for side effects. Although they cover standard path cases, this setup could lead to flakiness depending on external tool states or missing resources (e.g. Ansible assets) when running end-to-end tests that invoke internal commands.

## Evidence

- path: "tests/cli/backup.rs"
  loc: "line 22"
  note: "Test `backup_alias_bk_is_accepted` explicitly states it will fail due to missing ansible assets, proving that tests leak side effects instead of being isolated using ports/adapters."
- path: "tests/cli/switch.rs"
  loc: "line 28"
  note: "Tests like `switch_without_config_fails_gracefully` depend on global or local system state. A properly configured fake harness should be used for CLI interaction tests."
