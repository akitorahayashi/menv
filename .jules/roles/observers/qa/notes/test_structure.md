# Test Structure Analysis

## Overview
The repository employs a split testing strategy with distinct approaches for Python code and Ansible configuration. While service-layer unit tests are generally well-isolated, command-layer tests and integration tests exhibit significant architectural risks.

## Layers

### 1. Unit Tests (`tests/unit/`)
- **Scope:** Python services (`src/menv/services/`) and commands (`src/menv/commands/`).
- **Style:** Standard Pytest with `unittest.mock`.
- **Strengths:** Service tests (e.g., `ConfigDeployer`) use `tmp_path` and dependency injection effectively to isolate filesystem operations.
- **Weaknesses (Critical):**
    - **Unsafe Command Tests:** Tests for CLI commands (e.g., `TestConfigCommand` in `tests/unit/commands/test_config.py`) rely on the default dependency injection in `main.py`, causing them to execute against the **real user filesystem** (`~/.config/menv`). This is a "False Safety" anti-pattern.
    - **Missing Coverage:** The core logic for system modification (`AnsibleRunner`) is completely untested.
- **Risk:** Manual TOML serialization in `ConfigStorage` is a fragility point.

### 2. Integration Tests (`tests/intg/`)
- **Scope:** Ansible roles (`src/menv/ansible/`) and external resource validation.
- **Pattern A: "Mirror Logic" / Configuration Validation**
    - Tests (e.g., `tests/intg/roles/python/test_pipx_tools.py`) reimplement Ansible/Jinja2 logic (like regex replacements or version comparisons) in Python to verify configuration data.
    - **Pros:** Validates complex data generation (e.g., matrix generation).
    - **Cons:** Does not verify actual Ansible execution. If Python test logic and Jinja2 template logic diverge, tests pass while deployment fails.
- **Pattern B: External Validation**
    - `test_checksums.py` validates SHA256 sums of remote installer scripts.
    - **Risk:** Introduces unmarked, blocking network dependencies. Uses loop-based assertions, reducing failure diagnosability.
- **Pattern C: Integrity Checks**
    - `test_role_integrity.py` enforces static referential integrity. This is a strong "Shift Left" practice.

### 3. Missing Layers
- **Ansible Runtime Verification:** No tests execute `ansible-playbook` (not even in `--check` mode).
- **End-to-End (E2E):** No full system provisioning test.

## Infrastructure Gaps
- **Coverage Reporting:** No `pytest-cov` configuration; blind spots are not automatically detected.
- **Markers:** No `network` or `slow` markers to allow selective test execution.

## Recommendations
- **Refactor Command Tests:** Update `main.py` or test fixtures to support proper dependency injection overrides for CLI commands.
- **Deprecate Mirror Logic:** Replace Python reimplementations with simpler property checks or actual Ansible dry-runs.
- **Parametrize External Tests:** Refactor `test_checksums.py` to use `pytest.mark.parametrize` and add `network` markers.
- **Introduce Dry-Run:** Add `ansible-playbook --check` to the CI pipeline.
