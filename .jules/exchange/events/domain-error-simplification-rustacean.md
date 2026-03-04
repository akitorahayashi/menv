---
created_at: "2024-03-04"
author_role: "rustacean"
confidence: "medium"
---

## Statement

The application error handling model uses a manual implementation of `std::fmt::Display` and `std::error::Error` for `AppError`, whereas using a specialized library like `thiserror` would remove boilerplate, reduce errors, and compose meanings preserving their context effortlessly. Notably, `thiserror` is already downloaded as a crate as per `Cargo.toml`/`Cargo.lock` checks.

## Evidence

- path: "src/domain/error.rs"
  loc: "line 8-30"
  note: "Manual definition of `AppError` and subsequent manual implementations for `Display` and `Error` traits. Can be simplified using `#[derive(thiserror::Error)]`."
