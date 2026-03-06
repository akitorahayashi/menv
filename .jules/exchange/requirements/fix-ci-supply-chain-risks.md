---
label: "bugs"
implementation_ready: false
---

## Goal

Secure CI workflows by pinning exact versions for dependencies and GitHub actions, and implement a proper release workflow to a secure artifact registry.

## Problem

CI pipelines are exposed to non-determinism and supply-chain attacks. GitHub workflows rely on mutable version tags (`@v4`, `@v5`) for third-party actions instead of immutable commit SHAs. Furthermore, workflows dynamically install system packages via package managers without pinning toolchain versions. Lastly, the repository commits compiled bundled binaries directly back to the `main` branch rather than publishing to a secure artifact registry.

## Evidence

- source_event: "supply-chain-risk-mutable-tags-devops.md"
  path: ".github/actions/setup-base/action.yml"
  loc: "line 8, 13, 18, 22"
  note: "Uses mutable tags like actions/setup-python@v5, extractions/setup-just@v2, astral-sh/setup-uv@v5, Swatinem/rust-cache@v2."

- source_event: "supply-chain-risk-mutable-tags-devops.md"
  path: ".github/workflows/build-bundled-binary.yml"
  loc: "line 15, 34"
  note: "Uses mutable tags like actions/checkout@v4 and actions/upload-artifact@v4."

- source_event: "supply-chain-risk-mutable-tags-devops.md"
  path: ".github/workflows/sync-bundled-binary.yml"
  loc: "line 36, 44"
  note: "Uses mutable tags like actions/checkout@v4 and actions/download-artifact@v4."

- source_event: "unpinned-ci-dependencies-devops.md"
  path: ".github/workflows/run-linters.yml"
  loc: "line 20"
  note: "Runs `brew install shellcheck shfmt` without specifying toolchain versions."

- source_event: "unpinned-ci-dependencies-devops.md"
  path: ".github/workflows/collect-coverage.yml"
  loc: "line 29"
  note: "Runs `brew install mise` without specifying a tool version."

- source_event: "release-anti-pattern-bundled-binary-devops.md"
  path: ".github/workflows/sync-bundled-binary.yml"
  loc: "line 55-61"
  note: "Commits downloaded binary artifact directly to the main branch."

## Change Scope

- `.github/workflows/`
- `.github/actions/`

## Constraints

- Dependencies and execution tools must be deterministic and immune to upstream supply-chain mutations.
- Binary artifacts must not be committed directly to version control.

## Acceptance Criteria

- GitHub Actions are pinned to immutable commit SHAs instead of mutable version tags.
- Brew packages and other system dependencies in CI workflows specify exact version numbers.
- The `sync-bundled-binary.yml` workflow is refactored to publish to a proper release artifact registry (e.g., GitHub Releases) instead of committing to the `main` branch.
