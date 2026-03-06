---
created_at: "2026-03-06"
author_role: "tactician"
confidence: "high"
---

## Statement

A deeply nested, scope-local AGENTS.md file (`dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md`) is acting as a global contract, carrying extensive execution rules (Conduct, Design, Implementation, Documentation, Communication, Safety, User-specific) that logically apply to the entire repository. This violates the anti-pattern of global contracts carrying local execution rules, as well as the principle that rule ownership follows scope ownership.

## Evidence

- path: "dist/mev/ansible/roles/nodejs/config/common/coder/AGENTS.md"
  loc: "Entire file content (Lines 1-52)"
  note: "This file contains comprehensive project-wide rules (e.g., 'Ordered tasks are completed without interruption', 'Commands that discard uncommitted changes... are only run after explicit user approval') nested deeply within a specific Ansible role's config directory, creating ambiguous precedence and violating locality of rules."