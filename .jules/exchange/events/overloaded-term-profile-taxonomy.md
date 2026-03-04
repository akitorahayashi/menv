---
created_at: "2026-03-04"
author_role: "taxonomy"
confidence: "high"
---

## Statement

The term "profile" is overloaded and used for two distinct domain concepts: machine/environment targets (e.g., macbook, mac-mini) and user identities (e.g., personal, work).

## Evidence

- path: "src/domain/profile.rs"
  loc: "line 8 and 32"
  note: "Defines 'profile' as a machine-specific identifier (e.g., 'macbook', 'mac-mini') used for environment creation commands."
- path: "src/domain/vcs_identity.rs"
  loc: "line 4 and 13"
  note: "Defines 'switch profile' (e.g., 'personal', 'work') for VCS user identity resolution."
- path: "src/app/cli/make.rs"
  loc: "line 16-18"
  note: "CLI flag uses `profile` for machine selection (common, macbook/mbk)."
- path: "src/app/cli/switch.rs"
  loc: "line 11-12"
  note: "CLI flag uses `profile` for user identity selection (personal/p, work/w)."
