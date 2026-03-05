---
label: "bugs"
---

## Goal

Remove the anti-pattern of committing bundled binaries directly to the main branch via CI workflows.

## Problem

The release pipeline commits bundled binaries directly to the main branch rather than using an artifact registry or GitHub Releases. This conflates the source-of-truth branch with binary build artifacts, impacting Git performance and confusing provenance tracking.

## Affected Areas

### CI Workflows

- `.github/workflows/sync-bundled-binary.yml`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- External processes relying on finding the bundled binary directly in the repository tree at `dist/mev/bin/darwin-aarch64/mev` may fail.

## Acceptance Criteria

- The workflow pushing binary artifacts to the main branch is removed or refactored to use GitHub Releases or an artifact registry.

## Implementation Plan

1. Modify `.github/workflows/sync-bundled-binary.yml` to remove the steps that download the artifact and run `git add`, `git commit`, and `git push` to `dist/mev/bin/darwin-aarch64/mev`. Replace them with a step that creates a GitHub Release.
2. Verify the changes to `.github/workflows/sync-bundled-binary.yml` using `read_file`.
3. Run relevant tests using `cargo test`.
4. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.