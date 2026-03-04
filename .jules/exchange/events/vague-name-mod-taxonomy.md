---
created_at: "2026-03-04"
author_role: "taxonomy"
confidence: "medium"
---

## Statement

The codebase uses vague names like `AppContext` which violates the principle that names must not hide responsibility or be ambiguous. Using generic wrappers like `AppContext` without distinct domain nouns makes discovery harder.

## Evidence

- path: "src/app/context.rs"
  loc: "line 15-32"
  note: "`AppContext` holds domain ports (`AnsiblePort`, `ConfigStore`, `GitPort`, `JjPort`, etc.) and paths, functioning purely as a dependency container across all CLI commands without describing a distinct context."
