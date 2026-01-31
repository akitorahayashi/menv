# Test Structure Analysis

## Overview
The repository employs a split testing strategy with distinct approaches for Python code and Ansible configuration.

## Layers

### 1. Unit Tests (`tests/unit/`)
- **Scope:** Python services (`src/menv/services/`) and commands (`src/menv/commands/`).
- **Style:** Standard Pytest with `unittest.mock`.
- **Quality:** Generally high isolation. Good use of `tmp_path` fixture.
- **Risk:** Manual TOML serialization in `ConfigStorage` is a fragility point covered by unit tests but inherently risky.

### 2. Integration Tests (`tests/intg/`)
- **Scope:** Ansible roles and configuration (`src/menv/ansible/`).
- **Pattern:** "Mirror Logic" / Configuration Validation.
    - Tests reimplement Ansible/Jinja2 logic in Python to verify configuration files match expected patterns.
    - **Pros:** Validates complex configuration generation logic (e.g., matrix generation).
    - **Cons:** Does not verify actual Ansible behavior. Divergence between Python test logic and Jinja2 template logic is a major risk.
- **Integrity Checks:** `test_role_integrity.py` enforces static referential integrity (checking that referenced files exist). This is a strong "Shift Left" practice.

### 3. Missing Layers
- **Ansible Runtime Verification:** No tests execute `ansible-playbook` (not even in `--check` mode).
- **End-to-End (E2E):** No full system provisioning test. This is acceptable given the scope (local machine setup), but a dry-run is a missing middle ground.

## Recommendations
- **Maintain** the Integrity Checks as they provide fast feedback on structural errors.
- **Deprecate/Refactor** "Mirror Logic" tests where possible in favor of simpler property checks or actual dry-runs.
- **Introduce** `ansible-playbook --check` in the CI pipeline to catch runtime syntax/variable errors.
