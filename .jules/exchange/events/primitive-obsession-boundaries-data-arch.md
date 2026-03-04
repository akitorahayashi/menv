---
created_at: "2024-05-24"
author_role: "data_arch"
confidence: "high"
---

## Statement

The application exhibits primitive obsession at key boundaries, accepting primitive `&str` values for domain concepts like profiles and identities rather than leveraging type-safe domain models (e.g. Enums). This scatters validation logic, allows invalid states to be represented across boundaries, and obscures the Single Source of Truth for valid states.

## Evidence

- path: "src/app/api.rs"
  loc: "line 22, 29, 64"
  note: "Accepts `profile: &str` parameter in `create`, `make`, and `switch` APIs, bypassing boundary validation."
- path: "src/domain/profile.rs"
  loc: "line 32, 43"
  note: "Defines `validate_machine_profile(input: &str)` and `validate_profile(input: &str)` functions returning primitive `Result<&'static str, AppError>` instead of a strong Enum, shifting the validation burden to call sites."
- path: "src/domain/vcs_identity.rs"
  loc: "line 16"
  note: "Defines `resolve_switch_profile(input: &str)` returning primitive `Option<&'static str>` instead of a type-safe enum."
