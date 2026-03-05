---
label: "refacts"
---

## Goal

Resolve overloaded usage of the term 'profile' for both machine configurations and VCS user identities to eliminate ambiguity.

## Problem

The concept of 'Profile' is overloaded in the domain model, representing both hardware/machine targets and VCS user identities. This violates the Single Source of Truth and Boundary Sovereignty principles by conflating unrelated concepts under the same terminology and error types (`AppError::InvalidProfile`). The term "profile" is heavily overloaded in the CLI, used to describe both machine configurations (e.g., macbook, mac-mini) in the `create` and `make` commands, and VCS identities (e.g., personal, work) in the `switch` command.

## Affected Areas

### Core Domain

- `src/domain/profile.rs`
- `src/domain/vcs_identity.rs`
- `src/domain/error.rs`

### CLI Interface

- `src/app/cli/switch.rs`
- `src/app/cli/create.rs`
- `src/app/cli/make.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- Silent fallbacks are prohibited; any failure to resolve the new identity or profile terms must be explicitly surfaced.

## Risks

- Renaming 'profile' in CLI arguments might break existing scripts, aliases, or user workflows.
- Splitting `AppError::InvalidProfile` into separate error types might break downstream error handling or tests if not updated comprehensively.

## Acceptance Criteria

- 'Profile' is exclusively used for machine targets or configurations.
- The VCS identity concept is renamed to avoid using the word 'profile' (e.g., to 'Identity').
- The `switch` CLI command uses 'identity' instead of 'profile' for its argument/flag.
- `src/domain/error.rs` uses distinct error types for invalid machine profiles and invalid VCS identities (e.g., adding `AppError::InvalidIdentity`).
- All tests pass with the updated terminology.

## Implementation Plan

1. Update `src/domain/error.rs` to introduce a new `AppError::InvalidIdentity(String)` variant and retain `AppError::InvalidProfile` specifically for machine profiles.
2. Refactor `src/domain/vcs_identity.rs` to rename any references of 'Profile' to 'Identity' (e.g., rename constants, update docstrings, and change parsing logic to return `AppError::InvalidIdentity`).
3. Update `src/app/cli/switch.rs` to use `identity` instead of `profile` for the CLI argument, updating the Clap struct fields, help texts, and internal variable names accordingly.
4. Review `src/domain/profile.rs`, `src/app/cli/create.rs`, and `src/app/cli/make.rs` to ensure they exclusively use 'profile' in the context of machine targets, clarifying docstrings and help texts where appropriate.
5. Update all associated unit tests and integration tests in the affected files to align with the new terminology and error types.
