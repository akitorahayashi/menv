---
created_at: "2026-03-06"
author_role: "librarian"
confidence: "high"
---

## Statement

`README.md` contains flat accumulation of specialized content (Usage, Quick Start) at the top level, instead of serving as a cross-cutting entry point. This specialized content should be grouped into explicit subtrees within `docs/`.

## Evidence

- path: "README.md"
  loc: "## Quick Start, ## Usage"
  note: "Specialized procedural and usage documentation is placed in the top-level namespace, violating root namespace discipline."
