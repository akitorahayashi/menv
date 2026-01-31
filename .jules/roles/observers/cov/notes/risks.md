# Coverage & Testing Risks

## 1. Missing Coverage Infrastructure
**Observation:** The project lacks automated coverage collection (`pytest-cov`) and reporting.
**Risk:** Silent regression of test coverage; inability to identify untested critical paths.
**Evidence:** `pyproject.toml` lacks coverage dependencies.

## 2. Untested Critical Paths
**Observation:** `AnsibleRunner` (`src/menv/services/ansible_runner.py`) is the core mechanism for applying system changes via Ansible but has **zero** unit tests.
**Risk:** High probability of bugs in command construction or error handling leading to destructive actions or silent failures.
**Evidence:** Absence of `tests/unit/services/test_ansible_runner.py`.

## 3. False Safety & Environment Leakage
**Observation:** CLI tests (e.g., `tests/unit/commands/test_config.py`) execute against the real user filesystem (`~/.config/menv`) instead of an isolated test environment.
**Cause:** `src/menv/main.py` instantiates dependencies (like `ConfigStorage`) with default arguments inside the `main` callback, preventing `Typer`'s `CliRunner` from injecting mocks.
**Risk:**
  - Tests passing "by accident" due to user's local config.
  - Tests potentially modifying or deleting user's actual configuration.
**Evidence:** `src/menv/main.py` dependency injection pattern.
