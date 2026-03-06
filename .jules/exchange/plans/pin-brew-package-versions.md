---
label: "bugs"
---

## Goal

Secure CI workflows by pinning exact version numbers for system dependencies installed via package managers.

## Problem

CI pipelines dynamically install system packages via package managers (like Homebrew) without pinning toolchain versions, leading to non-determinism.

## Affected Areas

### GitHub Workflows

- `.github/workflows/run-linters.yml`
- `.github/workflows/collect-coverage.yml`

## Constraints

- Dependencies and execution tools must be deterministic and immune to upstream supply-chain mutations.

## Risks

- Pinned versions may become deprecated or unavailable in the package manager over time.

## Acceptance Criteria

- Brew packages and other system dependencies in CI workflows specify exact version numbers.

## Implementation Plan

1. Identify the current stable versions of `shellcheck`, `shfmt`, and `mise` available in Homebrew.
2. Update `.github/workflows/run-linters.yml` to specify exact versions for `shellcheck` and `shfmt` in the `brew install` command (e.g., `brew install shellcheck@<version> shfmt@<version>`).
3. Update `.github/workflows/collect-coverage.yml` to specify an exact version for `mise` in the `brew install` command (e.g., `brew install mise@<version>`).