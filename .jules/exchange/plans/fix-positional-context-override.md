---
label: "refacts"
---

## Goal

Refactor the `make` command's `profile` argument from a positional argument to an explicit option to separate target objects from context overrides.

## Problem

The `make` command defines `profile` as a positional argument rather than an explicit option, violating the structural separation of target objects and context overrides, which creates a rigid, over-parameterized interface.

## Affected Areas

### CLI Module

- `src/app/cli/make.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Risks

- Existing scripts or automated tooling that invoke `mev make <tag> <profile>` positionally will fail and need to be updated to `mev make <tag> --profile <profile>`.

## Acceptance Criteria

- The `profile` parameter is parsed as an explicit flag (e.g., `--profile`) rather than a positional argument.
- The CLI structural separation of objects and options is maintained.

## Implementation Plan

1. Modify `src/app/cli/make.rs` to update the `profile` field in the `MakeArgs` struct. Add the `#[arg(long, default_value = "common")]` macro attribute to convert it into an explicit option flag.
2. Search the codebase for any test cases or integrations that invoke the `make` command with a positional profile argument.
3. Update any discovered invocations to use the `--profile` flag format.
4. Run the test suite using `cargo test` to ensure that argument parsing works correctly and no regressions are introduced.