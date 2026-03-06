---
label: "bugs"
---

## Goal

Implement a proper release workflow to a secure artifact registry for compiled binaries.

## Problem

The repository commits compiled bundled binaries directly back to the `main` branch rather than publishing to a secure artifact registry, creating a release anti-pattern and polluting the version control history.

## Affected Areas

### GitHub Workflows

- `.github/workflows/sync-bundled-binary.yml`

## Constraints

- Binary artifacts must not be committed directly to version control.

## Risks

- Modifying the release process requires careful configuration of GitHub Release permissions.

## Acceptance Criteria

- The `sync-bundled-binary.yml` workflow is refactored to publish to a proper release artifact registry (e.g., GitHub Releases) instead of committing to the `main` branch.

## Implementation Plan

1. Modify `.github/workflows/sync-bundled-binary.yml` to remove the steps that commit the downloaded binary artifact to the `main` branch.
2. Add steps to upload the artifact to a GitHub Release using the GitHub CLI (`gh release upload`).
3. Ensure the workflow has the necessary `contents: write` permissions to create a release.