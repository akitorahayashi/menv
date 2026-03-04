---
created_at: "2026-03-04"
author_role: "tactician"
confidence: "high"
---

## Statement

The `src/AGENTS.md` file contains a "Architecture" table that duplicates the "Architecture" table found in the root `AGENTS.md` file. The local copy in `src/AGENTS.md` exhibits wording variances only without providing meaningful local scope differentiation. This violates the anti-pattern of duplicating directives across scopes with wording variance only.

## Evidence

- path: "src/AGENTS.md"
  loc: "5-15"
  note: "Contains the `## Architecture` table which is substantially the same as the table in the root `AGENTS.md` file, providing redundant structural background context."
- path: "AGENTS.md"
  loc: "8-18"
  note: "Contains the authoritative `## Architecture` table that defines the structural ownership and intent for the whole project."