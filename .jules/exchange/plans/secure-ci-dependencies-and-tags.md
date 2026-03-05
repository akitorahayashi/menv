---
label: "refacts"
---

## Goal

Pin toolchain component versions installed via Homebrew and use immutable commit SHAs for GitHub Actions rather than mutable tags.

## Problem

CI workflows currently use `brew install` for toolchain components without specifying versions, causing non-determinism. Additionally, the repository relies on mutable version tags for GitHub Actions instead of immutable commit SHAs, which introduces supply chain security risks and potential execution non-determinism.

## Affected Areas

### GitHub Actions and Workflows

- `.github/actions/setup-base/action.yml`
- `.github/workflows/run-linters.yml`
- `.github/workflows/build-bundled-binary.yml`
- `.github/workflows/collect-coverage.yml`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- GitHub Action references must be updated to use immutable commit SHAs.
- `brew install` steps in CI explicitly pin versions.

## Risks

- Hardcoded commit SHAs might become stale.
- Homebrew dependencies with pinned versions might become unavailable or incompatible over time.

## Acceptance Criteria

- All `brew install` commands in the CI workflows explicitly pin package versions.
- All GitHub actions `uses` directives refer to specific commit SHAs.

## Implementation Plan

1. Retrieve the latest commit SHAs for the currently used GitHub Actions (`actions/setup-python@v5`, `extractions/setup-just@v2`, `astral-sh/setup-uv@v5`, `Swatinem/rust-cache@v2`, `actions/checkout@v4`, `actions/upload-artifact@v4`).
2. Identify stable versions for `shellcheck`, `shfmt`, and `mise` in Homebrew.
3. Update `.github/actions/setup-base/action.yml` to replace mutable tags with commit SHAs. Verify changes using `read_file`.
4. Update `.github/workflows/run-linters.yml` to replace mutable tags with commit SHAs and pin versions for `shellcheck` and `shfmt` in the `brew install` command (e.g., `brew install shellcheck@<version> shfmt@<version>`). Verify changes using `read_file`.
5. Update `.github/workflows/build-bundled-binary.yml` to replace mutable tags with commit SHAs. Verify changes using `read_file`.
6. Update `.github/workflows/collect-coverage.yml` to replace mutable tags with commit SHAs and pin the version for `mise` in the `brew install` command. Verify changes using `read_file`.
7. Run relevant tests using `cargo test` to ensure project integrity.
8. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.