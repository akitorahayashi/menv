---
label: "docs"
implementation_ready: false
---

## Goal

Scaffold a foundational `docs/` directory, organize specialized content from the README, document missing testing strategies, and correct documentation drift regarding CLI commands.

## Problem

The repository currently lacks a foundational `docs/` directory, resulting in flat accumulation of human-facing documentation (Usage, Quick Start) in the `README.md`. Furthermore, `CONTRIBUTING.md` lacks baseline policies on testing strategies (e.g., domain logic tests must reside in `src/domain/`). Lastly, the README documents commands (`mev config set`, `mev config show`) that are actually implemented under the `mev identity` subcommand, demonstrating drift between documentation and implementation.

## Evidence

- source_event: "missing-docs-directory-librarian.md"
  path: "."
  loc: "/"
  note: "`docs/` directory is completely absent."

- source_event: "missing-testing-strategies-librarian.md"
  path: "CONTRIBUTING.md"
  loc: "## Contribution Policies"
  note: "Testing strategies and testing-related conventions are entirely omitted."

- source_event: "readme-contains-specialized-content-librarian.md"
  path: "README.md"
  loc: "## Quick Start, ## Usage"
  note: "Specialized procedural and usage documentation is placed in the top-level namespace."

- source_event: "readme-drift-config-identity-consistency.md"
  path: "README.md"
  loc: "Lines 58-63"
  note: "Documents `mev config set` and `mev config show` as valid commands instead of `mev identity`."

## Change Scope

- `docs/`
- `README.md`
- `CONTRIBUTING.md`

## Constraints

- `README.md` serves as a concise index linking to canonical documents in `docs/`.
- `CONTRIBUTING.md` must remain the authoritative, fully populated source for contribution policies.
- The documentation must conform to the implementation.
- Documentation must be written in a declarative style describing the current state.

## Acceptance Criteria

- A `docs/` directory is created with appropriate sub-documents (e.g., `docs/usage.md`, `docs/quick-start.md`).
- Usage and Quick Start sections are removed from `README.md` and replaced with links to the `docs/` directory.
- `CONTRIBUTING.md` includes explicit testing strategy policies.
- `README.md` is updated to reflect the correct `mev identity set` and `mev identity show` commands instead of `config`.
