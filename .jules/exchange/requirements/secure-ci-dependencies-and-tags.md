---
label: "bugs"
implementation_ready: false
---

## Goal

Pin toolchain component versions installed via Homebrew and use immutable commit SHAs for GitHub Actions rather than mutable tags.

## Problem

CI workflows use `brew install` for toolchain components without specifying specific versions or relying on a lockfile. This introduces non-determinism, as the installed versions depend on the current Homebrew catalog rather than the project's source of truth.

The repository utilizes mutable version tags (e.g., `@v4`, `@v5`) for GitHub Actions in multiple workflows and composite actions instead of immutable commit SHAs, which introduces a supply chain security risk and potential execution non-determinism.

## Evidence

- source_event: "unpinned-homebrew-dependencies-determinism-devops.md"
  path: ".github/workflows/run-linters.yml"
  loc: "23"
  note: "Installs `shellcheck` and `shfmt` via `brew install` without version pinning."
- source_event: "unpinned-homebrew-dependencies-determinism-devops.md"
  path: ".github/workflows/collect-coverage.yml"
  loc: "32"
  note: "Installs `mise` via `brew install` without version pinning."
- source_event: "mutable-action-tags-supply-chain-risk-devops.md"
  path: ".github/actions/setup-base/action.yml"
  loc: "8, 13, 16, 21"
  note: "Uses unpinned mutable tags for actions/setup-python@v5, extractions/setup-just@v2, astral-sh/setup-uv@v5, and Swatinem/rust-cache@v2."
- source_event: "mutable-action-tags-supply-chain-risk-devops.md"
  path: ".github/workflows/build-bundled-binary.yml"
  loc: "15, 36"
  note: "Uses unpinned mutable tags for actions/checkout@v4 and actions/upload-artifact@v4."
- source_event: "mutable-action-tags-supply-chain-risk-devops.md"
  path: ".github/workflows/run-linters.yml"
  loc: "15"
  note: "Uses unpinned mutable tags for actions/checkout@v4."

## Change Scope

- `.github/actions/setup-base/action.yml`
- `.github/workflows/run-linters.yml`
- `.github/workflows/build-bundled-binary.yml`
- `.github/workflows/collect-coverage.yml`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- `brew install` steps in CI explicitly pin versions.
- GitHub actions references are pinned to specific commit SHAs.
