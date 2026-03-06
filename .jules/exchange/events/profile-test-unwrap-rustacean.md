---
created_at: "2024-05-20"
author_role: "rustacean"
confidence: "high"
---

## Statement

Tests in `src/domain/profile.rs` rely on `unwrap()` directly in the test body instead of correctly propagating errors or using robust pattern matching. This masks failure context when assertions fail because `unwrap()` produces a panic trace instead of showing the underlying `Result` failure context.

## Evidence

- path: "src/domain/profile.rs"
  loc: "line 123"
  note: "`validate_machine_profile(\"macbook\").unwrap()` is used inside `validate_machine_profile_accepts_macbook` test."

- path: "src/domain/profile.rs"
  loc: "line 124"
  note: "`validate_machine_profile(\"mbk\").unwrap()` is used inside `validate_machine_profile_accepts_macbook` test."
