---
label: "refacts"
implementation_ready: false
---

## Goal

Eliminate primitive obsession at application boundaries by using strong Enum types instead of `&str` for domain concepts.

## Problem

The application exhibits primitive obsession at key boundaries, accepting primitive `&str` values for domain concepts like profiles and identities rather than leveraging type-safe domain models (e.g. Enums). This scatters validation logic, allows invalid states to be represented across boundaries, and obscures the Single Source of Truth for valid states.

## Evidence

- source_event: "primitive-obsession-boundaries-data-arch.md"
  path: "src/app/api.rs"
  loc: "line 22, 29, 64"
  note: "Accepts `profile: &str` parameter in `create`, `make`, and `switch` APIs, bypassing boundary validation."
- source_event: "primitive-obsession-boundaries-data-arch.md"
  path: "src/domain/profile.rs"
  loc: "line 32, 43"
  note: "Defines `validate_machine_profile(input: &str)` and `validate_profile(input: &str)` functions returning primitive `Result<&'static str, AppError>` instead of a strong Enum, shifting the validation burden to call sites."
- source_event: "primitive-obsession-boundaries-data-arch.md"
  path: "src/domain/vcs_identity.rs"
  loc: "line 16"
  note: "Defines `resolve_switch_profile(input: &str)` returning primitive `Option<&'static str>` instead of a type-safe enum."

## Change Scope

- `src/domain/vcs_identity.rs`
- `src/app/api.rs`
- `src/domain/profile.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- Public API boundaries (`src/app/api.rs`) accept domain Enums.
- Validation logic returns properly typed models rather than string references.
