---
created_at: "2026-03-04"
author_role: "structural_arch"
confidence: "high"
---

## Statement

The domain layer is leaking into the presentation/API layer, and `crate::domain` modules are importing from each other directly instead of through a clean facade or ports boundary, which risks creating tight coupling and cyclical dependencies. There's a violation of public surface minimization.

## Evidence

- path: "src/app/api.rs"
  loc: "14-18"
  note: "The `app::api` module uses `pub use crate::domain::...` to re-export internal domain details like `BackupTarget`, `AppError`, `ExecutionPlan`, `MevConfig`, and `VcsIdentity`, which breaks the boundary by making domain internals the public surface."
