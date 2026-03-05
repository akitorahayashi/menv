---
label: "refacts"
implementation_ready: false
---

## Goal

Rename generic `AppContext` to distinctly describe its domain responsibility, removing ambiguous naming.

## Problem

The codebase uses vague names like `AppContext` which violates the principle that names must not hide responsibility or be ambiguous. Using generic wrappers like `AppContext` without distinct domain nouns makes discovery harder.

## Evidence

- source_event: "vague-name-mod-taxonomy.md"
  path: "src/app/context.rs"
  loc: "line 15-32"
  note: "`AppContext` holds domain ports (`AnsiblePort`, `ConfigStore`, `GitPort`, `JjPort`, etc.) and paths, functioning purely as a dependency container across all CLI commands without describing a distinct context."

## Change Scope

- `src/app/context.rs`

## Constraints

- Changes must adhere to project principles such as avoiding ambiguous names, removing technical debt, and prioritizing systemic fixes.

## Acceptance Criteria

- The `AppContext` structure is renamed to something specific, like `DependencyContainer` or a context specific to its usage.
- All references in `src/app/context.rs` and dependent modules are updated.
