---
created_at: "2026-03-04"
author_role: "librarian"
confidence: "high"
---

## Statement

The `CONTRIBUTING.md` file incorrectly merges distinct document responsibilities by co-locating coding standards (policy) and verification commands (procedure) within the same file. This mixes policy and procedure and fails to separate concerns, violating the mandate that a document should have one distinct structural responsibility. These topics should be split into canonical documents under a dedicated documentation hierarchy.

## Evidence

- path: "CONTRIBUTING.md"
  loc: "lines 5-29"
  note: "Policy content declaring coding standards and naming conventions, representing static rules."
- path: "CONTRIBUTING.md"
  loc: "lines 31-41"
  note: "Procedural content mapping configuration files to their purposes, serving as orientation or reference."
- path: "CONTRIBUTING.md"
  loc: "lines 45-56"
  note: "Verification procedures and command invocations (`just check`, `just test`), which are dynamic actions distinct from coding policy."