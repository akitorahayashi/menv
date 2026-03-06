---
created_at: "2026-03-06"
author_role: "devops"
confidence: "high"
---

## Statement

The repository lacks an automated release workflow to a secure artifact registry, instead utilizing an anti-pattern of committing compiled bundled binaries directly back to the `main` branch.

## Evidence

- path: ".github/workflows/sync-bundled-binary.yml"
  loc: "line 55-61"
  note: "Commits and pushes the downloaded binary artifact directly to the main branch rather than publishing to a release registry."
