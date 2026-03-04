---
created_at: "2026-03-04"
author_role: "cov"
confidence: "high"
---

## Statement

Based on the `cargo tarpaulin` line coverage report (`just coverage`), critical domains such as Ansible execution paths, filesystem adapters, system backups, configuration creation, list commands, make commands, and app CLI execution are almost entirely uncovered. Overall line coverage is critically low at 18.39%. This represents a significant regression risk, particularly because these unverified paths orchestrate complex domain actions and interface directly with external state and user configurations.

## Evidence

- path: "src/app/cli/"
  loc: "0/313 lines"
  note: "CLI models and parsing logic (aider, shell, ssh, vcs, mod) lack line coverage entirely, creating risks of parsing errors or misconfigured user inputs crashing the application."
- path: "src/app/commands"
  loc: "31/393 lines"
  note: "Critical state transitions and user workflows like `create`, `list`, `make`, `deploy_configs`, and parts of `backup` and `config` are missing or have extremely low line coverage, jeopardizing system provisioning and orchestration safety."
- path: "src/app/api.rs"
  loc: "0/34 lines"
  note: "The API application layer orchestrator has zero line coverage, meaning the primary entry point linking domain models to adapter operations is unverified."
- path: "src/adapters"
  loc: "64/262 lines"
  note: "Key system integration layers, including the filesystem (`std_fs.rs`), vscode CLI, config store json parsing, and macos defaults CLI, are entirely untested or have low line coverage. Because adapters mutate system state and read files, lacking tests here risks silent IO failures or corrupted config parsing."
