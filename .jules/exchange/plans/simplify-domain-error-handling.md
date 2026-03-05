---
label: "refacts"
---

## Goal

Refactor AppError manual implementations of Display and Error to use the thiserror crate.

## Problem

The application error handling model uses a manual implementation of std::fmt::Display and std::error::Error for AppError. Using thiserror will remove boilerplate, reduce errors, and preserve context effortlessly.

## Affected Areas

### Domain Logic

- `src/domain/error.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- Removing manual Display implementations may slightly alter the output formatting if not perfectly replicated using thiserror formatting attributes, especially for conditional formatting in `AnsibleExecution`.

## Acceptance Criteria

- AppError utilizes #[derive(thiserror::Error)] and #[error(...)] attributes on its variants.
- Boilerplate manual implementations of Display and Error traits for AppError are removed.
- Tests pass after the refactoring.

## Implementation Plan

1. Read `src/domain/error.rs` to verify the exact structure of `AppError` and the manual `Display` and `Error` trait implementations using `read_file`.
2. Replace the manual trait implementations in `src/domain/error.rs` with `#[derive(thiserror::Error)]` on `AppError` and apply `#[error("...")]` to each variant matching the existing string formatting. Use `replace_with_git_merge_diff` for the modification.
3. Read `src/domain/error.rs` using `read_file` to verify that the changes were applied correctly.
4. Run `cargo test` in the workspace using `run_in_bash_session` to verify the code still compiles and tests pass.
5. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
