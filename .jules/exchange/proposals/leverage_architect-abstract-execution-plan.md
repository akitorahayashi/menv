---
role: "leverage_architect"
created_at: "2024-03-04"
title: "Abstract Execution Plan Serialization Phase"
---

## Problem

The system creates an `ExecutionPlan` structure containing a string vector of tags and profile names but immediately delegates to the `AnsibleAdapter` for side effects. This hides the actual scope of work from the user and makes verifying changes before running `create` or `make` impossible without examining the raw playbook files.

## Introduction

A strict "Plan & Apply" serialization boundary that resolves all nested tags, discovers roles, locates associated configuration directories, and validates required binaries before generating a finalized, immutable `ResolvedExecutionPlan`. This plan is fully separated from the execution engine.

## Importance

Decoupling intent resolution from side effect execution allows system users and automated tests to verify exactly what changes will be applied (e.g., via a `--dry-run` or `--plan` flag). This reduces unexpected destruction of user configurations and allows infrastructure changes to be reviewed statically.

## Impact Surface

- `ExecutionPlan` domain object will evolve to contain fully resolved tag expansions, configuration mappings, and dependency constraints.
- `AnsibleAdapter` will act strictly as an executor for `ResolvedExecutionPlan` rather than being partially responsible for expanding configuration roles during execution.
- `app/commands/create` and `make` will be split into planning and execution phases.

## Implementation Cost

Medium. The logic for expanding tags and mapping roles is already present within the `AnsibleAdapter`, but it must be hoisted into the domain layer and serialized before execution. It requires exposing `playbook.yml` semantics outside the Ansible adapter.

## Consistency Risks

- Risk of state staleness if the ansible roles or tags change between the planning phase and execution phase.
- Duplicating tag validation logic inside the rust application that overlaps with Ansible's native resolution, leading to a drift in what tags are actually supported vs mapped.

## Verification Signals

- Running `mev create --plan-only` produces a complete, deterministic, serializable summary of all roles, configs, and shell tools that will be provisioned without modifying the system.
- Integration tests can assert against generated plans without executing full ansible playbooks.
