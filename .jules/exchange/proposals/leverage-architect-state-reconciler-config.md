---
role: "leverage_architect"
created_at: "2024-03-04"
title: "Declarative State Reconciler for Configurations"
---

## Problem

Configuration commands (e.g., `switch`, `config create`) execute series of imperative side-effects against the host operating system, files, and VCS tools. A failure midway through deployment leaves the environment partially synchronized, requiring the user to run manual cleanup or force overwrite flags.

## Introduction

A configuration `StateReconciler` pattern that transitions the system from imperative function calls (`deploy_configs`, `run_config`) to a Desired State Model. The reconciler evaluates the target state against the current system state, creates a diff-based transaction plan, and executes it atomically (or implements strict rollback on failure).

## Importance

Eliminates the entire class of "partial configuration state" bugs. By formalizing configuration as a desired state declaration, the system guarantees that either all role configurations and identities are successfully deployed, or the system remains completely unchanged, significantly lowering operational anxiety and drag.

## Impact Surface

- The `commands/switch` and `commands/deploy_configs` modules will change from executing raw filesystem copies to building a state tree.
- Adapter ports (`FsPort`, `GitPort`, `JjPort`) will be refactored to support state interrogation (what is the current value?) and atomic execution.
- Replaces scattered, inline error handling with a centralized transaction commit boundary.

## Implementation Cost

High. It requires restructuring how `AppContext` commands interact with the underlying OS by introducing a generic state difference engine. It touches the core of how `.config/mev/` files and global tool configs are manipulated.

## Consistency Risks

- In-flight configuration deployments might fail if the host machine state changes concurrently during the reconciliation loop.
- The state tree model will need to correctly map Ansible role logic (e.g., recursive directory copy), increasing the initial surface area for filesystem logic bugs.

## Verification Signals

- Intentional failure injection during a multi-role configuration deployment results in 100% rollback of previous changes.
- Configuration status commands can natively report on "drift" between desired and actual state without executing side effects.
