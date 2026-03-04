---
role: "leverage_architect"
created_at: "2024-03-04"
title: "Unified Pre-flight Dependency Boundary"
---

## Problem

External command execution (e.g., `uv`, `git`, `jj`, `code`, `defaults`) is deeply embedded within adapter implementations. The application fails late in its execution lifecycle when system dependencies are absent, leaving the environment in an unknown or partially configured state.

## Introduction

A unified `SystemDependencyVerifier` service and `SystemEnvironmentPort` boundary introduced at the command planning layer. Instead of lazily verifying binaries via `which::which` or relying on subprocess failures mid-execution, all required external dependencies for an `ExecutionPlan` are statically requested and validated before any side effects begin.

## Importance

Eliminating late-stage execution failures fundamentally raises the reliability of the `mev` provisioning engine. It replaces scattered, unpredictable runtime crashes with a structured, early-feedback failure mode that immediately signals to the user exactly what prerequisite tools are missing.

## Impact Surface

- Adapters (AnsibleAdapter, GitCli, JjCli, VscodeCli) will expose their static dependency requirements.
- The `AppContext` or command orchestrators (e.g., `create`, `make`, `switch`) will integrate the verifier.
- The test suite will be expanded to validate system-level dependency mocking without executing subprocesses.

## Implementation Cost

Low. It requires defining a simple port (e.g., `SystemEnvironmentPort` with `has_binary(&str) -> bool`), creating an adapter (wrapping `which`), and updating existing adapter implementations to declare their dependencies rather than failing inline.

## Consistency Risks

- Temporary duplication during the transition phase if some adapters still rely on internal checks while the centralized verifier is implemented.
- The verifier might over-constrain the execution if not all tools are actually invoked by a specific subset of tags, requiring dynamic dependency resolution tied to the `ExecutionPlan`.

## Verification Signals

- Complete elimination of mid-execution subprocess panics due to `No such file or directory` or missing tools.
- A new pre-flight summary output is generated (or logged) that explicitly halts execution upfront when an environment is missing required binaries.
