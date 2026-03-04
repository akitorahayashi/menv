---
created_at: "2026-03-04"
author_role: "cli_sentinel"
confidence: "high"
---

## Statement

The CLI heavily overloads the term 'profile', using it to describe both machine configurations (e.g., macbook, mac-mini) in the `create` and `make` commands, and VCS identities (e.g., personal, work) in the `switch` command.

## Evidence

- path: "src/app/cli/create.rs"
  loc: "12-13"
  note: "Defines 'profile' as a positional argument representing a machine hardware configuration ('macbook', 'mac-mini')."
- path: "src/app/cli/switch.rs"
  loc: "12-13"
  note: "Defines 'profile' as a positional argument representing a VCS identity ('personal', 'work'), conflicting directly with the usage in `create.rs`."
