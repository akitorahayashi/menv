# Test Structure Analysis

## Overview
The `menv` repository employs a "Shift Left" testing strategy, prioritizing static analysis, unit testing, and configuration validation over traditional End-to-End (E2E) integration testing. This approach minimizes the cost and flakiness associated with testing system provisioning but introduces specific risks related to logic duplication.

## Test Levels

### 1. Static & Meta Analysis (High Coverage)
- **Tools:** `ansible-lint`, `ruff`, `mypy`, `shellcheck`.
- **Integrity Tests:** `tests/intg/test_role_integrity.py` validates that all file references in Ansible tasks exist in the repository.
- **Checksums:** `tests/intg/test_checksums.py` validates external asset integrity.
- **Value:** High. Catches broken links and syntax errors immediately.

### 2. Unit Tests (Pure Logic)
- **Location:** `tests/unit/`
- **Scope:** Covers the Python code in the `menv` CLI and services.
- **Technique:** Uses `unittest.mock` and `typer.testing.CliRunner` to isolate logic from filesystem and system side effects.
- **Value:** High. Ensures the CLI tool works as expected.

### 3. Configuration / "Integration" Tests (Data Validation)
- **Location:** `tests/intg/roles/`
- **Scope:** Validates the YAML configuration files (e.g., `tools.yml`, `pipx-tools.yml`) used by Ansible.
- **Technique:** **"Mirror Logic"**. Python tests reimplement the logic (e.g., Jinja2 filters, regex replacements) intended to be executed by Ansible to verify that the configuration data is compatible with that logic.
- **Value:** Medium/High. Ensures config data is valid, but does not verify the Ansible code itself.

## Risks & Observations
- **Mirror Logic Risk:** The "Integration" tests shadow the production logic. If the Ansible logic changes but the Python test logic doesn't (or vice versa), tests may pass while production fails.
- **No Runtime Verification:** There are no tests that execute the actual Ansible playbooks against a system. Runtime failures (e.g., package name changes, network issues, permission errors) are not caught by the test suite.
