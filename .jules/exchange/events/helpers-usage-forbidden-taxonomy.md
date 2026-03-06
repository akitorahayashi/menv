---
created_at: "2024-05-19"
author_role: "taxonomy"
confidence: "high"
---

## Statement

The codebase uses the ambiguous and strictly forbidden word "helpers" and "helper" in several places, primarily as command descriptions in the CLI layer and module documentation in both `mev` and `mev-internal` crates. This violates the architectural principle "No ambiguous names: core/, utils/, helpers/ are forbidden".

## Evidence

- path: "src/app/cli/mod.rs"
  loc: "67, 71, 79"
  note: "Doc comments use the ambiguous and forbidden term 'helpers'."
- path: "src/app/commands/backup/mod.rs"
  loc: "274"
  note: "Comment uses the term 'Shared helpers'."
- path: "crates/mev-internal/src/app/cli/mod.rs"
  loc: "23, 27, 35"
  note: "Doc comments use the term 'helpers' and 'helper'."
- path: "crates/mev-internal/src/app/cli/aider.rs"
  loc: "1"
  note: "Module doc comment uses 'helpers'."
- path: "crates/mev-internal/src/app/cli/shell.rs"
  loc: "1"
  note: "Module doc comment uses 'helper'."
- path: "crates/mev-internal/src/app/cli/vcs.rs"
  loc: "1"
  note: "Module doc comment uses 'helpers'."
