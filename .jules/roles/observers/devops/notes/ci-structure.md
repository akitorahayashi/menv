# CI/CD Structure

## Workflow Orchestration
- CI is driven by `.github/workflows/ci-workflows.yml` which triggers multiple parallel jobs:
  - `lint-and-test` (Reusable workflow)
  - `setup-*` (Reusable workflows for different environments)

## Task Execution
- `justfile` is the central entry point for local and CI tasks.
- `uv` is used for Python dependency management.
- `ruff` is used for Python linting/formatting.
- `ansible-lint` is used for Ansible roles.
- `shellcheck` and `shfmt` are used for shell scripts.

## Reusable Actions
- Local composite actions are defined in `.github/actions/`:
  - `setup-base`: Installs Python, just, uv, and syncs dependencies.
  - `install-jlo`: Installs the `jlo` CLI.
  - `configure-git`: Configures git identity.

## Jules Automation
- `.github/workflows/jules-workflows.yml` orchestrates the multi-agent system.
- It runs on a schedule (daily) or dispatch.
- It iterates through workstreams and layers (observers, deciders, planners, implementers).
- It relies on time-based waits (`sleep`) for async processing steps.
