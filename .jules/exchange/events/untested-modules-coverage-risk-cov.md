---
created_at: "2026-03-06"
author_role: "cov"
confidence: "high"
---

## Statement

Significant sections of core CLI commands have critical coverage gaps. Modules such as `backup/mod.rs`, `switch/mod.rs`, `create/mod.rs`, `config/mod.rs`, `list/mod.rs`, `make/mod.rs` and `execution_plan.rs` register 0.00% to 19.11% overall line coverage. These include critical decisions around system configurations, identity assignments, and execution planning where silent failures or uncaught errors could severely impact system state. In particular, execution_plan.rs has 0% coverage and creates an ansible plan. There are no tests evaluating whether execution plans are constructed with the right tags for standard setup runs.

## Evidence


- path: "src/app/commands/switch/mod.rs"
  loc: "execute()"
  note: "This module controls identity switching logic globally using a git client, and yet records 0% coverage, meaning no tests handle scenarios where a system identity configuration switch fails or behaves unexpectedly."
- path: "src/app/commands/create/mod.rs"
  loc: "execute()"
  note: "Command orchestration that coordinates deploying configurations and ansible runbook steps has 0% line coverage, meaning regression tests on ansible playbook calls do not exist."
- path: "src/app/commands/backup/mod.rs"
  loc: "execute_system(), execute_vscode(), execute()"
  note: "Backup system functionality execution functions are completely untested (0% execution module coverage), raising the risk that back up targets will silently fail to backup important settings."
- path: "src/domain/execution_plan.rs"
  loc: "ExecutionPlan::full_setup()"
  note: "Core domain function responsible for fetching FULL_SETUP_TAGS for execution setup has 0 coverage."
