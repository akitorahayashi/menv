---
created_at: "2024-03-06"
author_role: "consistency"
confidence: "high"
---

## Statement

The README.md documents `mev config set` and `mev config show` as commands to configure and show VCS identities. However, these commands are actually implemented under `mev identity set` and `mev identity show`. The `config` command only has a `create` subcommand. This is a drift between documented behavior and the current implementation.

## Evidence

- path: "README.md"
  loc: "Lines 58-63"
  note: "Documents `mev config set` and `mev config show` as valid commands."
- path: "src/app/cli/config.rs"
  loc: "Enum `ConfigCommand`"
  note: "The `ConfigCommand` enum only contains the `Create` variant, proving `set` and `show` are not implemented here."
- path: "src/app/cli/identity.rs"
  loc: "Enum `IdentityCommand`"
  note: "The `IdentityCommand` enum contains the `Show` and `Set` variants, proving this is where the functionality actually resides."
