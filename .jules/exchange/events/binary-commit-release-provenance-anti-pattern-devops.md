---
created_at: "2026-03-04"
author_role: "devops"
confidence: "high"
---

## Statement

The release pipeline commits bundled binaries directly to the `main` branch rather than using an artifact registry or GitHub Releases. This conflates the source-of-truth branch with binary build artifacts, impacting Git performance and confusing provenance tracking.

## Evidence

For multi-file events, add multiple list items.

- path: ".github/workflows/sync-bundled-binary.yml"
  loc: "59, 60, 61, 62"
  note: "Downloads binary artifact and directly runs `git add`, `git commit`, and `git push` to add `dist/mev/bin/darwin-aarch64/mev` back into the main branch."
