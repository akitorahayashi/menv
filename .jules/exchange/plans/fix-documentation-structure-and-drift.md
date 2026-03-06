---
label: "docs"
---

## Goal

Scaffold a foundational `docs/` directory, organize specialized content from the README, document missing testing strategies, and correct documentation drift regarding CLI commands.

## Problem

The repository currently lacks a foundational `docs/` directory, resulting in flat accumulation of human-facing documentation (Usage, Quick Start) in the `README.md`. Furthermore, `CONTRIBUTING.md` lacks baseline policies on testing strategies (e.g., domain logic tests must reside in `src/domain/`). Lastly, the README documents commands (`mev config set`, `mev config show`) that are actually implemented under the `mev identity` subcommand, demonstrating drift between documentation and implementation.

## Affected Areas

### Documentation

- `docs/`
- `README.md`
- `CONTRIBUTING.md`

## Constraints

- `README.md` serves as a concise index linking to canonical documents in `docs/`.
- `CONTRIBUTING.md` must remain the authoritative, fully populated source for contribution policies.
- The documentation must conform to the implementation.
- Documentation must be written in a declarative style describing the current state.
- Documentation for LLMs (e.g., AGENTS.md, CLAUDE.md) must be kept concise for token efficiency.
- Declarative updates must preserve existing content and integrate new material without duplication or complete replacement.
- Do not use bold emphasis (**) in Markdown. Use hierarchy and headings for organization.

## Risks

- Links in `README.md` to `docs/` may be broken if filenames do not match.
- Information loss during the migration of content from `README.md` to `docs/`.

## Acceptance Criteria

- A `docs/` directory is created.
- `docs/usage.md` is created containing the Usage section from `README.md`, with commands updated (`mev identity set` and `mev identity show`).
- `docs/quick-start.md` is created containing the Quick Start section from `README.md`.
- `README.md` Usage and Quick Start sections are replaced with links to the new documents.
- `CONTRIBUTING.md` includes explicit testing strategy policies: "Domain logic tests reside as self-contained unit tests within their respective `src/domain/` modules inside a `#[cfg(test)]` block. Redundant logic coverage in external `tests/library/` integration tests is avoided."

## Implementation Plan

1. Create directory `docs/`.
2. Extract the "Quick Start" section from `README.md` and write it to `docs/quick-start.md`. Ensure heading levels are adjusted if necessary.
3. Extract the "Usage" section from `README.md` and write it to `docs/usage.md`. Update the configuration commands from `mev config set` and `mev config show` to `mev identity set` and `mev identity show`. Note: `mev config create` commands should remain as they deploy role configs.
4. Update `README.md` to replace the extracted sections with a concise index linking to `docs/quick-start.md` and `docs/usage.md`.
5. Update `CONTRIBUTING.md` to add a new "Testing Strategies" subsection under "Contribution Policies" detailing the required placement of domain logic tests.