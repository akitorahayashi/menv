---
created_at: "2026-03-04"
author_role: "tactician"
confidence: "high"
---

## Statement

The `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md` file contains repository-wide conduct, design, and implementation rules that are not specific to its local scope (`nodejs` role config for `coder`). This violates the "ownership boundary" constraint where rule ownership must follow scope ownership and global contracts must not carry local execution rules (or vice versa).

## Evidence

- path: "dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md"
  loc: "1-40"
  note: "This file contains sections like `## Conduct`, `### Design`, `### Implementation`, `### Documentation`, and `### Communication`, which describe global repository rules rather than nodejs/coder-specific behavior."