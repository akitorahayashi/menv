# CI/CD Architecture

## Overview
The project uses GitHub Actions for CI/CD, heavily relying on the `menv` CLI tool and `just` task runner for executing setup and verification steps.

## Key Components

### Workflows
- **`ci-workflows.yml`**: The main entry point for CI on Push/PR. It triggers multiple reusable workflows.
- **`lint-and-test.yml`**: Runs `just test` (unit/integration) and `just check` (linting/formatting).
- **`setup-*.yml`**: A family of workflows (setup-python, setup-nodejs, etc.) that verify the `menv` CLI's ability to provision environments.
- **`jules-workflows.yml`**: Orchestrates the Jules agent layers using a schedule and sleep-based delays.

### Tooling
- **`just`**: Used as the primary task runner. The `Justfile` defines recipes for `test`, `check`, `fix`, and wrapping `menv` commands.
- **`uv`**: Used for Python dependency management and environment creation (`uv sync`, `uv venv`).
- **`menv`**: The application under test, also used to drive the setup steps in CI.

## Observations & Anti-Patterns

### Reproducibility
- **Floating Tags**: `macos-latest` and `ubuntu-latest` are used in some workflows, while `macos-15` is used in others.
- **Unpinned Dependencies**: `brew install shellcheck` installs the latest version. GitHub Actions are pinned to major versions (`@v4`, `@v5`) instead of SHAs.
- **Silent Failures**: The `justfile` suppresses errors for `shfmt` (`|| true`), which is not installed in the CI environment.

### Orchestration
- **Sleep-based Waiting**: `jules-workflows.yml` uses `sleep` to wait for agent processing, which is inefficient and fragile.
- **Scattered Setup**: Setup logic is duplicated between `lint-and-test.yml` and `setup-python.yml` (e.g., `uv` venv creation).

### Artifacts
- **No Build Artifacts**: The pipelines currently run scripts and verifications but do not produce immutable artifacts (e.g., binaries, containers) for promotion. The "artifact" is implicitly the source code or the PyPI package (not yet seen in release workflow).
- **Violation of "Ship Artifacts, Not Scripts"**: Without a build step producing a versioned artifact (e.g., Wheel, PEX), deployments rely on checking out source code, which risks "prod is different" drift and makes rollback difficult.
