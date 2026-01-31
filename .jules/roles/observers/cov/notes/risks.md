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
**Observation:** CLI tests execute against the real user filesystem (`~/.config/menv`) instead of an isolated test environment. This is a systemic issue affecting `test_config.py`, `test_make.py`, `test_create.py`, and likely others.
**Cause:** `src/menv/main.py` instantiates dependencies (like `ConfigStorage`, `PlaybookService`, `AnsiblePaths`) with default arguments inside the `main` callback. The tests use `CliRunner` to invoke the app directly, which triggers this hardcoded dependency injection, bypassing any attempts at mocking.
**Risk:**
  - Tests passing "by accident" due to the developer's local environment configuration (e.g., `test_make.py` reading the real installed playbook).
  - Tests potentially modifying or deleting user's actual configuration (`test_config.py`).
**Evidence:**
  - `src/menv/main.py` dependency injection pattern.
  - `tests/unit/commands/test_config.py` relying on user config state.
  - `tests/unit/commands/test_make.py` reading installed playbook.
