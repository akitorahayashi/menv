---
label: "tests"
implementation_ready: false
---

## Goal

Remove redundant domain logic tests in the `library_contracts` module that duplicate unit test assertions.

## Problem

Redundant domain logic testing: The project has redundant tests verifying standard library integration within pure logic testing, e.g. mapping simple string enums over CLI logic. The `library_contracts` tests re-verify the same behavior that is verified in unit tests within the `domain` module, adding maintenance overhead without providing meaningful new guarantees.

## Evidence

- source_event: "redundant-domain-tests-qa.md"
  path: "tests/library/backup_target.rs"
  loc: "line 4"
  note: "Tests `backup_target_resolves_system` duplicate testing logic that should reside in `src/domain/backup_target.rs` unit tests (which lacks them, but the logic is entirely pure domain logic)."
- source_event: "redundant-domain-tests-qa.md"
  path: "tests/library/domain_exports.rs"
  loc: "line 5"
  note: "Tests `domain_profile_types_are_public` explicitly test resolution logic that is already tested in `src/domain/profile.rs` unit tests (`resolves_canonical_profiles`), testing identical inputs and outputs."

## Change Scope

- `tests/library/backup_target.rs`
- `tests/library/domain_exports.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- Redundant tests in `tests/library/` are removed.
- Unit tests in `src/domain/` are confirmed to cover the required logic exclusively.
