---
created_at: "2026-03-06"
author_role: "tactician"
confidence: "high"
---

## Statement

The `crates/mev-internal/AGENTS.md` file specifies commands for verifying the crate (`cargo fmt`, `cargo clippy`, `cargo test`) but does not include the essential structural context that these commands must be executed within the `crates/mev-internal` directory (since it is not part of the root cargo workspace). This unguarded failure path will cause the verification commands to fail if executed from the repository root.

## Evidence

- path: "crates/mev-internal/AGENTS.md"
  loc: "Lines 17-21"
  note: "Lists `cargo test --all-targets --all-features` and other verifications under 'Verify Commands' without the requisite working directory constraint (`cd crates/mev-internal`). A user or agent following these rules blindly from the project root will encounter errors as this crate is not a member of the root workspace."