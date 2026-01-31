# Structural Map

## Overview
The `menv` project adheres to a strict Domain-Driven Design (DDD) inspired structure, enforcing separation of concerns through explicit layers (CLI, Services, Protocols, Models, Ansible).

## Directory Structure Analysis

### Python Package (`src/menv/`)
- **Commands (`commands/`)**:
  - One file per command.
  - Dependencies flow strictly from `commands` -> `context/services`.
  - No logic in `__init__.py`.
- **Services (`services/`)**:
  - One class per file.
  - Implements corresponding `Protocol`.
  - Injected via `AppContext`.
  - No backward dependencies on `commands`.
- **Protocols (`protocols/`)**:
  - Defines interfaces for services.
  - Ensures decoupling between consumers and implementations.
- **Models (`models/`)**:
  - Pure data structures.
  - One file per domain.
- **Ansible (`ansible/`)**:
  - Self-contained package resource.
  - Accessed via `AnsiblePaths` service.

### Ansible Roles (`src/menv/ansible/roles/`)
- **Domain-Based**: Roles are organized by domain (e.g., `python`, `rust`, `system`, `brew`), avoiding generic buckets like `utils`.
- **Configuration**:
  - Centralized in `config/common` and `config/profiles`.
  - Deployed to `~/.config/menv` by `ConfigDeployer`.
- **Tasks**:
  - Granular task files included by `main.yml`.
  - No global shared utilities found; dependencies are explicit (e.g., `system` role).

### Tests (`tests/`)
- **Unit (`unit/`)**:
  - Mirrors package structure (`commands`, `services`).
  - Uses mocks.
- **Integration (`intg/`)**:
  - Validates `playbook.yml` integrity and role existence.
  - Ensures structural constraints (e.g., unique tags).
- **Mocks (`mocks/`)**:
  - One class per file.
  - Implements `Protocol`.

## Adherence to Principles
- **Dependency Direction**: Strictly respected. Commands depend on Context/Services. Services depend on Protocols.
- **Cohesion**: High. Files are grouped by change reason (domain).
- **Findability**: Excellent. Predictable 1:1 mapping between concept and file location.
- **Public Surface**: `menv` package exports minimal surface. `main.py` is the clear entry point.
- **Unidirectional Flow**: CLI -> Command -> Context -> Service -> Ansible/System.

## Violations
No structural violations were found during the analysis. The codebase strictly follows the guidelines defined in `AGENTS.md`.
