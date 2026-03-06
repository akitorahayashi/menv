---
label: "refacts"
implementation_ready: false
---

## Goal

Enforce distinct boundaries by removing direct domain layer re-exports in the API module and abstracting filesystem concepts from domain pure logic ports.

## Problem

The `app::api` module re-exports components directly from the domain layer instead of mapping them, causing tight coupling between external callers and internal domain structures. Furthermore, the domain layer leaks I/O concerns by directly relying on `std::path::Path` and `std::path::PathBuf` in `fs.rs` and `identity_store.rs`, making it harder to test pure business rules in isolation.

## Evidence

- source_event: "app-layer-mesh-coupling-structural-arch.md"
  path: "src/app/api.rs"
  loc: "line 14-19"
  note: "Directly re-exports domain models, tightly coupling external callers to internal structures."

- source_event: "domain-io-entanglement-structural-arch.md"
  path: "src/domain/ports/fs.rs"
  loc: "line 3, 16"
  note: "Directly uses std::path::Path and std::path::PathBuf in domain port definition."

- source_event: "domain-io-entanglement-structural-arch.md"
  path: "src/domain/ports/identity_store.rs"
  loc: "line 3, 23"
  note: "Directly uses std::path::PathBuf in identity store port definition."

## Change Scope

- `src/app/api.rs`
- `src/domain/ports/fs.rs`
- `src/domain/ports/identity_store.rs`

## Constraints

- The codebase employs a Hexagonal Architecture, strictly separating logic into `src/domain/` (pure rules and ports) and `src/app/`.
- Domain pure logic must not entangle with file system concepts.

## Acceptance Criteria

- `src/app/api.rs` maps domain models to API-specific structs rather than directly re-exporting them.
- `src/domain/ports/fs.rs` and `src/domain/ports/identity_store.rs` abstract file paths away from `std::path` types into pure domain string/identifier representations where appropriate, or adapt appropriately to remove `std::path` from pure domain definition.
