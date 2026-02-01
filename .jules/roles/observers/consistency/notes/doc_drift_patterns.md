# Documentation Drift Patterns

## Observed Patterns

### 1. Phantom Documentation
Documentation (e.g., `README.md`) references commands or features that do not exist in the codebase.
- **Example:** `menv introduce --help` is listed in `README.md` but the `introduce` command is not registered in `src/menv/main.py`.
- **Risk:** Users attempt to run documented commands and fail, eroding trust in documentation.

### 2. Inaccurate Examples
Internal documentation (docstrings) provides usage examples that contradict the actual CLI registration.
- **Example:** `src/menv/commands/make.py` docstring uses `menv make list`, but the command is registered as `menv list` (or `menv ls`) in `src/menv/main.py`.
- **Risk:** Developers relying on docstrings for usage info will be misled.

### 3. Unverified Wrappers
CLI command wrappers invoke backend scripts without adhering to the script's interface, causing runtime failures.
- **Example:** `menv backup` wrapper (`src/menv/commands/backup.py`) fails to pass the required `config_dir` argument to the underlying backend scripts (`scripts/system/backup-system.py`), causing them to crash.
- **Root Cause:** Lack of integration tests verifying the end-to-end execution of CLI wrappers.
