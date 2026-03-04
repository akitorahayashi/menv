---
label: "refacts"
implementation_ready: false
---

## Goal

Refactor `AppError` manual implementations of `Display` and `Error` to use the `thiserror` crate.

## Problem

The application error handling model uses a manual implementation of `std::fmt::Display` and `std::error::Error` for `AppError`, whereas using a specialized library like `thiserror` would remove boilerplate, reduce errors, and compose meanings preserving their context effortlessly. Notably, `thiserror` is already downloaded as a crate as per `Cargo.toml`/`Cargo.lock` checks.

## Evidence

- source_event: "domain-error-simplification-rustacean.md"
  path: "src/domain/error.rs"
  loc: "line 8-30"
  note: "Manual definition of `AppError` and subsequent manual implementations for `Display` and `Error` traits. Can be simplified using `#[derive(thiserror::Error)]`."

## Change Scope

- `src/domain/error.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- `AppError` utilizes `#[derive(thiserror::Error)]`.
- Boilerplate manual implementations are removed.
