---
created_at: "2026-03-06"
author_role: "cov"
confidence: "high"
---

## Statement

The current failure threshold for `cargo tarpaulin` is set arbitrarily at 40%, and current test coverage stands significantly below it at 19.11%, leading to constant test failures on standard `just coverage` checks.

## Evidence


- path: "coverage/cobertura.xml"
  loc: "line-rate=19.11%"
  note: "Tarpaulin execution result shows 19.11% overall line coverage, while the gate expects 40%."
- path: "Justfile"
  loc: "coverage recipe"
  note: "Shows an unaddressed issue in repository CI gating where minimum code quality expectations are disjointed from current state."
