---
# Changes Summary Schema
#
# Authoritative schema for .jules/exchange/changes.md.
#
# Purpose: advisory summary of recent codebase activity for downstream layers.
# Observers use these entries to decide whether a change falls within their
# responsibility. Each entry must be self-contained and actionable.
#
# Exactly 5 entries are required. If fewer than 5 distinct themes exist,
# group minor changes under a broader theme to fill all slots.

created_at: "2026-03-04"
---

## Summaries

### Rust CLI Migration & Core Rewriting

Scope: src/app/cli/, src/app/commands/, src/menv/commands/, tests/cli/, tests/unit/commands/

Impact: Core CLI commands (`list`, `make`, `switch`, `update`) migrated from Python to Rust, establishing a stable CLI entry point. Python implementations and their tests were removed, significantly reducing legacy code and standardizing command execution under Rust.

### Ports and Adapters Restructuring

Scope: src/adapters/, src/domain/ports/, src/menv/services/, src/menv/protocols/

Impact: Replaced Python services and protocols with Rust-based ports and adapters (e.g., `AnsiblePort`, `GitPort`, `JjPort`, `FsPort`). Python service logic (e.g., `AnsibleRunner`, `ConfigDeployer`) was removed. This unifies external system integrations and improves type safety and testability in the core domain.

### Backup Orchestration Refactoring

Scope: src/domain/backup_target.rs, src/app/commands/backup/, src/menv/commands/backup/

Impact: Introduced a `BackupTarget` enum in the Rust domain to orchestrate backup logic, replacing the legacy Python `BackupTarget` dataclasses and scripts. Obsolete Python backup implementation and mock services were removed, streamlining the backup domain.

### Domain Purification and Identity Extraction

Scope: src/domain/vcs_identity.rs, src/app/api.rs, src/domain/ports/config_store.rs

Impact: Refactored VCS identity usage by introducing a `VcsIdentity` model with profile resolution capabilities. Cleaned up domain boundaries by isolating identity configuration concerns from the broader application state, leading to a purer domain layer.

### CI Workflows and Dependency Optimization

Scope: .github/workflows/, .github/actions/, Cargo.lock, pyproject.toml, uv.lock

Impact: Optimized continuous integration pipelines by restructuring jobs (e.g., consolidating test-and-lint), removing `continue-on-error` from coverage, locking the `cargo-tarpaulin` version with `mise`, and updating tool versions (e.g., `jlo` v15.1.3). This enhances build determinism and execution speed.
