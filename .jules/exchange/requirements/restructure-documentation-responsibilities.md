---
label: "docs"
implementation_ready: false
---

## Goal

Establish a distinct documentation hierarchy by creating a `docs/` directory and untangling mixed responsibilities in root documents like README and CONTRIBUTING.

## Problem

The repository lacks a dedicated `docs/` directory, forcing all documentation, regardless of responsibility, to accumulate at the top-level namespace. This violates the architectural principle that the root namespace is scarce and reserved for cross-cutting entry points, and it necessitates scaffolding a structural foundation from scratch.

The `CONTRIBUTING.md` file incorrectly merges distinct document responsibilities by co-locating coding standards (policy) and verification commands (procedure) within the same file. This mixes policy and procedure and fails to separate concerns, violating the mandate that a document should have one distinct structural responsibility. These topics should be split into canonical documents under a dedicated documentation hierarchy.

The `README.md` file inappropriately mixes structural responsibilities by co-locating orientation content (project purpose and architecture) with detailed procedural instructions (installation, distribution synchronization, and exhaustive usage commands). This violates the principle that one document must have one structural responsibility, inflating navigation cost and hiding placement intent.

The `src/AGENTS.md` file contains a "Architecture" table that duplicates the "Architecture" table found in the root `AGENTS.md` file. The local copy in `src/AGENTS.md` exhibits wording variances only without providing meaningful local scope differentiation. This violates the anti-pattern of duplicating directives across scopes with wording variance only.

The `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md` file contains repository-wide conduct, design, and implementation rules that are not specific to its local scope (`nodejs` role config for `coder`). This violates the "ownership boundary" constraint where rule ownership must follow scope ownership and global contracts must not carry local execution rules (or vice versa).

## Evidence

- source_event: "missing-docs-directory-librarian.md"
  path: "docs/"
  loc: "directory level"
  note: "Directory does not exist, confirming the absence of a structured documentation foundation."
- source_event: "missing-docs-directory-librarian.md"
  path: "."
  loc: "top-level"
  note: "The top-level contains multiple Markdown files (`README.md`, `CONTRIBUTING.md`, `AGENTS.md`) without a dedicated subtree for specialized content, indicating a flat accumulation anti-pattern."
- source_event: "contributing-mixed-responsibilities-librarian.md"
  path: "CONTRIBUTING.md"
  loc: "lines 5-29"
  note: "Policy content declaring coding standards and naming conventions, representing static rules."
- source_event: "contributing-mixed-responsibilities-librarian.md"
  path: "CONTRIBUTING.md"
  loc: "lines 31-41"
  note: "Procedural content mapping configuration files to their purposes, serving as orientation or reference."
- source_event: "contributing-mixed-responsibilities-librarian.md"
  path: "CONTRIBUTING.md"
  loc: "lines 45-56"
  note: "Verification procedures and command invocations (`just check`, `just test`), which are dynamic actions distinct from coding policy."
- source_event: "readme-mixed-responsibilities-librarian.md"
  path: "README.md"
  loc: "lines 1-4"
  note: "Orientation content outlining the project purpose and Rust-first architecture."
- source_event: "readme-mixed-responsibilities-librarian.md"
  path: "README.md"
  loc: "lines 6-27"
  note: "Procedural content providing detailed prerequisites and installation steps, which should reside in specialized documentation."
- source_event: "readme-mixed-responsibilities-librarian.md"
  path: "README.md"
  loc: "lines 35-86"
  note: "Exhaustive command reference and usage procedures that clutter the cross-cutting entry point and should be separated into a distinct specification or procedural guide."
- source_event: "duplicated-architecture-context-tactician.md"
  path: "src/AGENTS.md"
  loc: "5-15"
  note: "Contains the `## Architecture` table which is substantially the same as the table in the root `AGENTS.md` file, providing redundant structural background context."
- source_event: "duplicated-architecture-context-tactician.md"
  path: "AGENTS.md"
  loc: "8-18"
  note: "Contains the authoritative `## Architecture` table that defines the structural ownership and intent for the whole project."
- source_event: "misplaced-global-rules-tactician.md"
  path: "dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md"
  loc: "1-40"
  note: "This file contains sections like `## Conduct`, `### Design`, `### Implementation`, `### Documentation`, and `### Communication`, which describe global repository rules rather than nodejs/coder-specific behavior."

## Change Scope

- `docs/`
- `AGENTS.md`
- `README.md`
- `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`
- `CONTRIBUTING.md`
- `src/AGENTS.md`
- `.`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- A `docs/` directory is created.
- Procedural, orientation, and policy content are separated into dedicated, single-responsibility files.
- Global rules misplaced in local directories and duplicated architecture context in AGENTS.md are removed.
