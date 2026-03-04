---
created_at: "2026-03-04"
author_role: "devops"
confidence: "high"
---

## Statement

The repository utilizes mutable version tags (e.g., `@v4`, `@v5`) for GitHub Actions in multiple workflows and composite actions instead of immutable commit SHAs, which introduces a supply chain security risk and potential execution non-determinism.

## Evidence

For multi-file events, add multiple list items.

- path: ".github/actions/setup-base/action.yml"
  loc: "8, 13, 16, 21"
  note: "Uses unpinned mutable tags for actions/setup-python@v5, extractions/setup-just@v2, astral-sh/setup-uv@v5, and Swatinem/rust-cache@v2."
- path: ".github/workflows/build-bundled-binary.yml"
  loc: "15, 36"
  note: "Uses unpinned mutable tags for actions/checkout@v4 and actions/upload-artifact@v4."
- path: ".github/workflows/run-linters.yml"
  loc: "15"
  note: "Uses unpinned mutable tags for actions/checkout@v4."
