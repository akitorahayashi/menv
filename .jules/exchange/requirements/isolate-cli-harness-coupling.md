---
label: "tests"
implementation_ready: false
---

## Goal

Decouple CLI tests from system state by utilizing isolated seams for side effects rather than relying directly on `harness::TestContext` running actual commands.

## Problem

The CLI tests are tightly coupled to the system state via `harness::TestContext`, which uses actual commands like `cli().assert().success()` without isolated seams for side effects. Although they cover standard path cases, this setup could lead to flakiness depending on external tool states or missing resources (e.g. Ansible assets) when running end-to-end tests that invoke internal commands.

## Evidence

- source_event: "cli-harness-coupling-qa.md"
  path: "tests/cli/backup.rs"
  loc: "line 22"
  note: "Test `backup_alias_bk_is_accepted` explicitly states it will fail due to missing ansible assets, proving that tests leak side effects instead of being isolated using ports/adapters."
- source_event: "cli-harness-coupling-qa.md"
  path: "tests/cli/switch.rs"
  loc: "line 28"
  note: "Tests like `switch_without_config_fails_gracefully` depend on global or local system state. A properly configured fake harness should be used for CLI interaction tests."

## Change Scope

- `tests/cli/switch.rs`
- `tests/cli/backup.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- Tests do not rely on missing assets or local system state.
- A properly configured fake harness or isolated adapter layer is utilized for CLI interaction tests.
