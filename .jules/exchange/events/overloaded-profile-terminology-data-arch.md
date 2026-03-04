---
created_at: "2024-05-24"
author_role: "data_arch"
confidence: "high"
---

## Statement

The concept of 'Profile' is overloaded in the domain model, representing both hardware/machine targets and VCS user identities. This violates the Single Source of Truth and Boundary Sovereignty principles by conflating unrelated concepts under the same terminology and error types (`AppError::InvalidProfile`).

## Evidence

- path: "src/domain/profile.rs"
  loc: "line 6, 9"
  note: "Defines 'Profile' as hardware/machine targets (`MACHINE_PROFILES`, `VALID_PROFILES` including 'common', 'macbook', 'mac-mini')."
- path: "src/domain/vcs_identity.rs"
  loc: "line 12, 16"
  note: "Defines 'Profile' as VCS user identities (`SWITCH_PROFILES` including 'personal', 'work')."
- path: "src/domain/error.rs"
  loc: "line 11"
  note: "Shares the same `AppError::InvalidProfile(String)` error for both machine profiles and VCS identity profiles."
