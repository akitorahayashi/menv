---
label: "tests"
---

## Goal

Remove redundant domain logic tests in the `library_contracts` module that duplicate unit test assertions.

## Problem

Redundant domain logic testing: The project has redundant tests verifying standard library integration within pure logic testing, e.g. mapping simple string enums over CLI logic. The `library_contracts` tests re-verify the same behavior that is verified in unit tests within the `domain` module, adding maintenance overhead without providing meaningful new guarantees.

## Affected Areas

### Tests

- `tests/library/backup_target.rs`
- `tests/library/domain_exports.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- Removing tests without ensuring equivalent coverage in the domain module could lead to regressions in domain logic testing.

## Acceptance Criteria

- Redundant tests in `tests/library/` are removed.
- Unit tests in `src/domain/` are confirmed to cover the required logic exclusively.

## Implementation Plan

1. Migrate missing unit tests to `src/domain/backup_target.rs` (such as checking `backup_target_resolves_system` logic, as the requirement notes it currently lacks them but the logic is pure domain logic).
2. Remove `backup_target_resolves_system` from `tests/library/backup_target.rs`.
3. Verify `resolves_canonical_profiles` exists and covers identical inputs/outputs in `src/domain/profile.rs`.
4. Remove `domain_profile_types_are_public` from `tests/library/domain_exports.rs`.
5. Run unit tests to verify domain module logic is completely covered and no regressions are introduced.
