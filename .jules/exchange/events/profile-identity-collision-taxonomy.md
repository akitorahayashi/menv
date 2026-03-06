---
created_at: "2024-05-19"
author_role: "taxonomy"
confidence: "high"
---

## Statement

The term "Profile" is used incorrectly in the CLI output of the `mev identity show` command to refer to VCS user identities (personal, work). In the domain and rest of the codebase, "Profile" strictly refers to machine hardware configurations (macbook, mac-mini, common). This blurs the domain concepts and violates the naming consistency principles.

## Evidence

- path: "src/app/commands/identity/mod.rs"
  loc: "23"
  note: "`println!(\"{:<12} {:<20} Email\", \"Profile\", \"Name\");` uses the word 'Profile' to label 'personal' and 'work' identities, contradicting the repository's strict separation of these concepts."
- path: "src/domain/profile.rs"
  loc: "7-25"
  note: "Defines `Profile` enum strictly for hardware/machine targets."
- path: "src/domain/vcs_identity.rs"
  loc: "15-20"
  note: "Defines `SwitchIdentity` enum for user targets (Personal, Work)."
