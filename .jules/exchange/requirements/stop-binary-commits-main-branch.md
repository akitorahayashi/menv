---
label: "bugs"
implementation_ready: false
---

## Goal

Remove the anti-pattern of committing bundled binaries directly to the `main` branch via CI workflows.

## Problem

The release pipeline commits bundled binaries directly to the `main` branch rather than using an artifact registry or GitHub Releases. This conflates the source-of-truth branch with binary build artifacts, impacting Git performance and confusing provenance tracking.

## Evidence

- source_event: "binary-commit-release-provenance-anti-pattern-devops.md"
  path: ".github/workflows/sync-bundled-binary.yml"
  loc: "59, 60, 61, 62"
  note: "Downloads binary artifact and directly runs `git add`, `git commit`, and `git push` to add `dist/mev/bin/darwin-aarch64/mev` back into the main branch."

## Change Scope

- `.github/workflows/sync-bundled-binary.yml`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- The workflow pushing binary artifacts to the main branch is removed or refactored to use GitHub Releases or an artifact registry.
