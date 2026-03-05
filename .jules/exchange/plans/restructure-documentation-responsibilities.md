---
label: "docs"
---

## Goal

Establish a distinct documentation hierarchy by creating a `docs/` directory and untangling mixed responsibilities in root documents like README and CONTRIBUTING.

## Problem

The repository lacks a dedicated `docs/` directory, forcing all documentation, regardless of responsibility, to accumulate at the top-level namespace. This violates the architectural principle that the root namespace is scarce and reserved for cross-cutting entry points, and it necessitates scaffolding a structural foundation from scratch.

The `CONTRIBUTING.md` file incorrectly merges distinct document responsibilities by co-locating coding standards (policy) and verification commands (procedure) within the same file. This mixes policy and procedure and fails to separate concerns, violating the mandate that a document should have one distinct structural responsibility. These topics should be split into canonical documents under a dedicated documentation hierarchy.

The `README.md` file inappropriately mixes structural responsibilities by co-locating orientation content (project purpose and architecture) with detailed procedural instructions (installation, distribution synchronization, and exhaustive usage commands). This violates the principle that one document must have one structural responsibility, inflating navigation cost and hiding placement intent.

The `src/AGENTS.md` file contains a "Architecture" table that duplicates the "Architecture" table found in the root `AGENTS.md` file. The local copy in `src/AGENTS.md` exhibits wording variances only without providing meaningful local scope differentiation. This violates the anti-pattern of duplicating directives across scopes with wording variance only.

The `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md` file contains repository-wide conduct, design, and implementation rules that are not specific to its local scope (`nodejs` role config for `coder`). This violates the "ownership boundary" constraint where rule ownership must follow scope ownership and global contracts must not carry local execution rules (or vice versa).

## Affected Areas

### Documentation Files

- `docs/`
- `AGENTS.md`
- `README.md`
- `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`
- `CONTRIBUTING.md`
- `src/AGENTS.md`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.
- Declarative updates must preserve existing content without duplication or complete replacement.
- Development-related documentation is written in English.
- The documentation must conform to the implementation, and the implementation must not be modified to conform to the documentation.
- Documentation for LLMs (AGENTS.md, CLAUDE.md, etc.) is kept concise for token efficiency.
- Documentation is written in a declarative style describing the current state. Imperative or changelog-style descriptions are prohibited.
- Do not use bold emphasis (**) in Markdown. Use hierarchy and headings for organization.

## Risks

- Links inside documentation or external references to specific headers in `README.md` or `CONTRIBUTING.md` might be broken if content is completely removed instead of correctly pointed to the new dedicated files in `docs/`.

## Acceptance Criteria

- A `docs/` directory is created.
- Procedural, orientation, and policy content are separated into dedicated, single-responsibility files inside `docs/` or respective locations.
- Global rules misplaced in local directories (`dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`) and duplicated architecture context in `src/AGENTS.md` are removed.

## Implementation Plan

1. Create a `docs/` directory at the root of the repository.
2. Create `docs/usage.md` and `docs/installation.md` (or combine appropriately) and move procedural instructions (installation, synchronization, and usage commands) from `README.md` into them. Update `README.md` to link to these new files.
3. Create `docs/policy.md` and `docs/procedure.md` (or similar clear names) and move the coding standards from `CONTRIBUTING.md` into `docs/policy.md` and verification commands to `docs/procedure.md`. Update `CONTRIBUTING.md` to link to the new files.
4. Remove the redundant "Architecture" table from `src/AGENTS.md`.
5. Remove the global repository rules from `dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`, or remove the file entirely if it has no local scope directives left.
