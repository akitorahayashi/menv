---
label: "refacts"
---

## Goal

Consolidate redundant implementations of `copy_dir_recursive` into a single shared capability to adhere to the Single Source of Truth principle.

## Problem

A recursive directory copy function is redundantly implemented in both `src/app/commands/deploy_configs.rs` and `src/app/commands/config/mod.rs`. This duplicates logic across boundaries, forcing future bug fixes or changes to be mirrored manually.

## Affected Areas

### Source Code

- `src/domain/ports/fs.rs`
- `src/adapters/fs/std_fs.rs`
- `src/app/commands/deploy_configs.rs`
- `src/app/commands/config/mod.rs`

## Constraints

- Duplicate logic must be consolidated to a single source of truth within the existing domain/ports architecture.
- Both call sites must handle their specific error context, while `FsPort::copy_dir_recursive` should return `AppError::Io`.

## Risks

- Breaking the `deploy` or `config` commands if the consolidated function does not handle directory creation correctly.

## Acceptance Criteria

- `copy_dir_recursive` logic is added to `FsPort` trait in `src/domain/ports/fs.rs`.
- `copy_dir_recursive` is implemented in `StdFs` in `src/adapters/fs/std_fs.rs`.
- `src/app/commands/deploy_configs.rs` and `src/app/commands/config/mod.rs` use the new shared function.
- Tests pass.

## Implementation Plan

1. Modify `src/domain/ports/fs.rs`
   - Add `fn copy_dir_recursive(&self, src: &std::path::Path, dst: &std::path::Path) -> Result<(), crate::domain::error::AppError>;` to the `FsPort` trait.
2. Modify `src/adapters/fs/std_fs.rs`
   - Implement `copy_dir_recursive` in the `StdFs` implementation for `FsPort`.
   - Ensure the implementation mimics the recursive logic currently found in the codebase. The implementation should rely on `std::fs` operations (e.g., `std::fs::create_dir_all`, `std::fs::read_dir`, `std::fs::copy`) and map errors to `AppError::Io`.
3. Refactor `src/app/commands/deploy_configs.rs`
   - Remove the `copy_dir_recursive` public function.
   - Inject or access `FsPort` in the `deploy_for_tags` flow (e.g., via `crate::app::DependencyContainer` or passing `&dyn FsPort` as a parameter if not already available) and replace the local function call with `fs.copy_dir_recursive(src, dst)`. Add a custom error check for `!src.is_dir()` if needed before calling, to preserve the existing specific `AppError::Config` error message.
4. Refactor `src/app/commands/config/mod.rs`
   - Remove the `copy_dir_recursive` private function.
   - Replace the local function call with `fs.copy_dir_recursive(src, dst)` using the injected `FsPort` instance from the `AppContext`.
5. Verify changes
   - Run `cargo check` and `cargo test` to ensure compilation succeeds and tests pass without regressions.
