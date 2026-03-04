---
created_at: "2026-03-04"
author_role: "librarian"
confidence: "high"
---

## Statement

The `README.md` file inappropriately mixes structural responsibilities by co-locating orientation content (project purpose and architecture) with detailed procedural instructions (installation, distribution synchronization, and exhaustive usage commands). This violates the principle that one document must have one structural responsibility, inflating navigation cost and hiding placement intent.

## Evidence

- path: "README.md"
  loc: "lines 1-4"
  note: "Orientation content outlining the project purpose and Rust-first architecture."
- path: "README.md"
  loc: "lines 6-27"
  note: "Procedural content providing detailed prerequisites and installation steps, which should reside in specialized documentation."
- path: "README.md"
  loc: "lines 35-86"
  note: "Exhaustive command reference and usage procedures that clutter the cross-cutting entry point and should be separated into a distinct specification or procedural guide."