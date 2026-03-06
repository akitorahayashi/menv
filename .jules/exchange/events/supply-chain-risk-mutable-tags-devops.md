---
created_at: "2026-03-06"
author_role: "devops"
confidence: "high"
---

## Statement

Multiple CI workflows and composite actions rely on mutable version tags (e.g., `@v4`, `@v5`) for third-party actions instead of immutable commit SHAs, exposing the verification path to supply-chain attacks.

## Evidence

- path: ".github/actions/setup-base/action.yml"
  loc: "line 8, 13, 18, 22"
  note: "Uses mutable tags like actions/setup-python@v5, extractions/setup-just@v2, astral-sh/setup-uv@v5, Swatinem/rust-cache@v2."
- path: ".github/workflows/build-bundled-binary.yml"
  loc: "line 15, 34"
  note: "Uses mutable tags like actions/checkout@v4 and actions/upload-artifact@v4."
- path: ".github/workflows/sync-bundled-binary.yml"
  loc: "line 36, 44"
  note: "Uses mutable tags like actions/checkout@v4 and actions/download-artifact@v4."
