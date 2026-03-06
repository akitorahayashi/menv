---
label: "bugs"
---

## Goal

Secure CI workflows by pinning all third-party GitHub Actions to immutable commit SHAs.

## Problem

GitHub workflows currently rely on mutable version tags (e.g., `@v4`, `@v5`) for third-party actions instead of immutable commit SHAs, exposing CI pipelines to non-determinism and supply-chain attacks.

## Affected Areas

### GitHub Actions and Workflows

- `.github/actions/setup-base/action.yml`
- `.github/workflows/build-bundled-binary.yml`
- `.github/workflows/sync-bundled-binary.yml`
- `.github/workflows/run-linters.yml`
- `.github/workflows/collect-coverage.yml`
- `.github/workflows/run-tests.yml`

## Constraints

- Dependencies and execution tools must be deterministic and immune to upstream supply-chain mutations.

## Risks

- Upgrading to new major/minor versions of actions requires manually updating the SHA and testing compatibility.

## Acceptance Criteria

- All third-party GitHub Actions in `.github/workflows/` and `.github/actions/` are pinned to immutable commit SHAs instead of mutable version tags.

## Implementation Plan

1. Use a tool to resolve the current version tags to their respective commit SHAs for all third-party actions.
2. Replace the mutable tags (`@v4`, `@v5`, etc.) with the resolved SHAs in all `.github/workflows/*.yml` and `.github/actions/*/action.yml` files.