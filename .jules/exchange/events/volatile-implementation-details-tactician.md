---
created_at: "2026-03-06"
author_role: "tactician"
confidence: "high"
---

## Statement

The `dist/mev/ansible/roles/rust/AGENTS.md` file rests on volatile implementation details rather than durable structural guidance. It enumerates exact tools (`gho`, `jlo`, `kpv`, `mx`, `pure`, `ssv`), file formats, and URL patterns which are ephemeral operational details, rather than providing the background context and constraints that are execution-critical. This violates the rule to exclude volatile implementation trivia from AGENTS.md.

## Evidence

- path: "dist/mev/ansible/roles/rust/AGENTS.md"
  loc: "Lines 11-15"
  note: "Enumerates the exact process of URL construction ('https://github.com/<repo>/releases/download/<tag>/<name>-<os>-<arch>'), listing explicit tool names ('gho', 'jlo', etc.), and an asset naming convention. These are volatile implementation specifics of the Ansible role and should not be stored as an agent contract."