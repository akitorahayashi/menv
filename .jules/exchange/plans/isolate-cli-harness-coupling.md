---
label: "tests"
---

## Goal

Decouple CLI tests from system state by utilizing isolated seams for side effects rather than relying directly on `harness::TestContext` running actual commands.

## Problem

The CLI tests are tightly coupled to the system state via `harness::TestContext`, which uses actual commands like `cli().assert().success()` without isolated seams for side effects. Although they cover standard path cases, this setup could lead to flakiness depending on external tool states or missing resources (e.g. Ansible assets) when running end-to-end tests that invoke internal commands.

## Affected Areas

### tests

- `tests/cli/switch.rs`
- `tests/cli/backup.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- Breaking existing test coverage or changing test assumptions.
- Tests may become too disconnected from reality if mocks are misconfigured.

## Acceptance Criteria

- Tests do not rely on missing assets or local system state.
- A properly configured fake harness or isolated adapter layer is utilized for CLI interaction tests.

## Implementation Plan

1. Create an isolated adapter or fake harness inside `tests/harness/` or utilize an existing one to intercept and mock command execution side effects.
2. Refactor `tests/cli/backup.rs` to replace the tight coupling in tests like `backup_alias_bk_is_accepted` to use the new isolated harness instead of failing due to missing system state.
3. Refactor `tests/cli/switch.rs` to replace tests that depend on system state (e.g. `switch_without_config_fails_gracefully`) with the isolated harness.
4. Verify tests pass deterministically without requiring local machine resources.
