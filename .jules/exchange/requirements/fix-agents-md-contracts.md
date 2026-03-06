---
label: "docs"
implementation_ready: true
---

## Goal

Ensure AGENTS.md files contain strictly scoped, structural guidance without volatile implementation details or ambiguous global rules.

## Problem

AGENTS.md rules are incorrectly scoped: a deep nested role file (`nodejs/config/common/coder/AGENTS.md`) defines global rules, while `crates/mev-internal/AGENTS.md` lacks the critical context that its verify commands must be run within its specific directory. Additionally, the Rust role `AGENTS.md` is populated with volatile implementation details (e.g., exact URLs and tool names) rather than durable structural constraints.

## Evidence

- source_event: "global-rules-in-deep-scope-tactician.md"
  path: "dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md"
  loc: "Entire file content (Lines 1-52)"
  note: "Contains comprehensive project-wide rules nested deeply within a specific Ansible role's config directory."

- source_event: "missing-working-directory-constraint-tactician.md"
  path: "crates/mev-internal/AGENTS.md"
  loc: "Lines 17-21"
  note: "Lists `cargo test` verify commands without the requisite working directory constraint (`cd crates/mev-internal`)."

- source_event: "volatile-implementation-details-tactician.md"
  path: "dist/mev/ansible/roles/rust/AGENTS.md"
  loc: "Lines 11-15"
  note: "Enumerates exact URL construction, specific tool names, and asset naming conventions which are volatile implementation specifics."

## Change Scope

- `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`
- `crates/mev-internal/AGENTS.md`
- `dist/mev/ansible/roles/rust/AGENTS.md`

## Constraints

- AGENTS.md files must enforce strict scoped rules; global contracts must not be placed in deep, scope-local directories.
- Volatile implementation details are prohibited in AGENTS.md unless execution-critical.

## Acceptance Criteria

- The global rules in the `nodejs` coder `AGENTS.md` are removed or moved to the root `AGENTS.md`.
- `crates/mev-internal/AGENTS.md` includes instructions to `cd crates/mev-internal` before running verify commands.
- The Rust role `AGENTS.md` is stripped of volatile URL structures and exact tool names, focusing on structural constraints instead.
