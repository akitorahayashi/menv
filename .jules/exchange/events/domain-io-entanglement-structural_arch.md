---
created_at: "2026-03-06"
author_role: "structural_arch"
confidence: "high"
---

## Statement

The domain layer contains multiple ports that leak I/O concerns into the pure domain logic. Specifically, `fs.rs` and `identity_store.rs` rely on `std::path::Path` and `std::path::PathBuf`, rather than abstracting these concepts entirely away from the pure business rules. This violates the dependency direction rules by entangling core logic with file system concepts, making it harder to test domain logic purely in-memory or swap out configuration mechanisms entirely.

## Evidence


- path: "src/domain/ports/fs.rs"
  loc: "line 3, 16"
  note: "Directly uses std::path::Path and std::path::PathBuf in domain port definition."
- path: "src/domain/ports/identity_store.rs"
  loc: "line 3, 23"
  note: "Directly uses std::path::PathBuf in identity store port definition, assuming configuration must exist on a file path."
