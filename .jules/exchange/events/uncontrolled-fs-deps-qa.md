---
created_at: "2024-03-06"
author_role: "qa"
confidence: "high"
---

## Statement

Tests rely on `std::fs` operations interacting directly with the filesystem rather than isolating I/O boundaries. The testing context fails to utilize abstract/mocked filesystems resulting in uncontrolled side effects.

## Evidence

- path: "tests/harness/test_context.rs"
  loc: "std::fs::create_dir_all"
  note: "TestContext heavily relies on global standard library operations, mutating state directly to create files for testing without I/O boundaries."
- path: "src/adapters/identity_store/local_json.rs"
  loc: "impl IdentityStore for IdentityFileStore"
  note: "Tightly coupled to `std::fs`, limiting isolation during tests as operations mutate disk directly."
