---
created_at: "2026-03-06"
author_role: "structural_arch"
confidence: "high"
---

## Statement

The `app::api` module re-exports components directly from the domain layer (like `Profile` and `BackupTarget`) instead of acting as a distinct Facade boundary. This means that external callers (such as `main.rs` or tests) are tightly coupled to the internal domain structures. Changes to the internal domain models can immediately break API consumers, because the API module leaks these models rather than mapping them.

## Evidence


- path: "src/app/api.rs"
  loc: "line 14-19"
  note: "Directly re-exports `BackupTarget`, `Error`, `ExecutionPlan`, `IdentityState`, `Profile`, and `VcsIdentity` using `pub use crate::domain::...`."
