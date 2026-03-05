---
label: "refacts"
implementation_ready: false
---

## Goal

Resolve overloaded usage of the term 'profile' for both machine configurations and VCS user identities to eliminate ambiguity.

## Problem

The concept of 'Profile' is overloaded in the domain model, representing both hardware/machine targets and VCS user identities. This violates the Single Source of Truth and Boundary Sovereignty principles by conflating unrelated concepts under the same terminology and error types (`AppError::InvalidProfile`).

The term "profile" is overloaded and used for two distinct domain concepts: machine/environment targets (e.g., macbook, mac-mini) and user identities (e.g., personal, work).

The CLI heavily overloads the term 'profile', using it to describe both machine configurations (e.g., macbook, mac-mini) in the `create` and `make` commands, and VCS identities (e.g., personal, work) in the `switch` command.

## Evidence

- source_event: "overloaded-profile-terminology-data-arch.md"
  path: "src/domain/profile.rs"
  loc: "line 6, 9"
  note: "Defines 'Profile' as hardware/machine targets (`MACHINE_PROFILES`, `VALID_PROFILES` including 'common', 'macbook', 'mac-mini')."
- source_event: "overloaded-profile-terminology-data-arch.md"
  path: "src/domain/vcs_identity.rs"
  loc: "line 12, 16"
  note: "Defines 'Profile' as VCS user identities (`SWITCH_PROFILES` including 'personal', 'work')."
- source_event: "overloaded-profile-terminology-data-arch.md"
  path: "src/domain/error.rs"
  loc: "line 11"
  note: "Shares the same `AppError::InvalidProfile(String)` error for both machine profiles and VCS identity profiles."
- source_event: "overloaded-term-profile-taxonomy.md"
  path: "src/domain/profile.rs"
  loc: "line 8 and 32"
  note: "Defines 'profile' as a machine-specific identifier (e.g., 'macbook', 'mac-mini') used for environment creation commands."
- source_event: "overloaded-term-profile-taxonomy.md"
  path: "src/domain/vcs_identity.rs"
  loc: "line 4 and 13"
  note: "Defines 'switch profile' (e.g., 'personal', 'work') for VCS user identity resolution."
- source_event: "overloaded-term-profile-taxonomy.md"
  path: "src/app/cli/make.rs"
  loc: "line 16-18"
  note: "CLI flag uses `profile` for machine selection (common, macbook/mbk)."
- source_event: "overloaded-term-profile-taxonomy.md"
  path: "src/app/cli/switch.rs"
  loc: "line 11-12"
  note: "CLI flag uses `profile` for user identity selection (personal/p, work/w)."
- source_event: "overloaded-terminology-cli-sentinel.md"
  path: "src/app/cli/create.rs"
  loc: "12-13"
  note: "Defines 'profile' as a positional argument representing a machine hardware configuration ('macbook', 'mac-mini')."
- source_event: "overloaded-terminology-cli-sentinel.md"
  path: "src/app/cli/switch.rs"
  loc: "12-13"
  note: "Defines 'profile' as a positional argument representing a VCS identity ('personal', 'work'), conflicting directly with the usage in `create.rs`."

## Change Scope

- `src/domain/profile.rs`
- `src/domain/error.rs`
- `src/app/cli/switch.rs`
- `src/app/cli/create.rs`
- `src/domain/vcs_identity.rs`
- `src/app/cli/make.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- 'Profile' is exclusively used for machine targets or VCS identity, with the other concept renamed (e.g., 'Identity').
- The CLI arguments and corresponding domain models are updated to reflect the disambiguation.
