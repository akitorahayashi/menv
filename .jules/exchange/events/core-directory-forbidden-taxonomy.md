---
created_at: "2024-05-19"
author_role: "taxonomy"
confidence: "high"
---

## Statement

The codebase uses an ambiguous and explicitly forbidden directory name 'core' inside the shell ansible role configuration. The repository's `AGENTS.md` strictly forbids using ambiguous names such as `core/`, `utils/`, and `helpers/`.

## Evidence

- path: "dist/mev/ansible/roles/shell/config/common/alias/core"
  loc: "directory path"
  note: "Uses the forbidden ambiguous name 'core', violating the repository's naming conventions explicitly stated in AGENTS.md."
