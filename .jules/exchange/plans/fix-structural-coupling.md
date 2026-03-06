---
label: "refacts"
---

## Goal

Enforce distinct boundaries by removing direct domain layer re-exports in the API module and abstracting filesystem concepts from domain pure logic ports.

## Problem

The `app::api` module re-exports components directly from the domain layer instead of mapping them, causing tight coupling between external callers and internal domain structures. Furthermore, the domain layer leaks I/O concerns by directly relying on `std::path::Path` and `std::path::PathBuf` in `fs.rs` and `identity_store.rs`, making it harder to test pure business rules in isolation.

## Affected Areas

### API Layer
- `src/app/api.rs`

### Domain Ports
- `src/domain/ports/fs.rs`
- `src/domain/ports/identity_store.rs`

## Constraints

- The codebase employs a Hexagonal Architecture, strictly separating logic into `src/domain/` (pure rules and ports) and `src/app/`.
- Domain pure logic must not entangle with file system concepts.

## Risks

- Breaking changes to external consumers of the API module if mappings omit necessary fields.
- Potential regressions in file system and identity storage operations if `std::path` abstraction is incorrect.

## Acceptance Criteria

- `src/app/api.rs` maps domain models to API-specific structs rather than directly re-exporting them.
- `src/domain/ports/fs.rs` and `src/domain/ports/identity_store.rs` abstract file paths away from `std::path` types into pure domain string/identifier representations where appropriate, or adapt appropriately to remove `std::path` from pure domain definition.

## Implementation Plan

1. In `src/app/api.rs`, remove `pub use crate::domain::...` lines. Define wrapper structs/enums for the previously re-exported domain types, and update API functions to return/accept these mapped structs. Provide `From` implementations to convert between domain and API models.
2. In `src/domain/ports/fs.rs`, change arguments from `&Path` to `&str` (or custom pure domain types) and return types from `PathBuf` to `String`.
3. In `src/domain/ports/identity_store.rs`, update `identity_path` to return a `String` rather than `PathBuf`.
4. Update the adapter implementations in `src/adapters/` (e.g., `src/adapters/fs/std_fs.rs`, `src/adapters/identity_store/local_json.rs`) to satisfy the new port traits.
5. Fix any compilation errors in tests and the rest of the application resulting from these changes.