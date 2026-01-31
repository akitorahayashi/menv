# Menv Project Structure

The `menv` project is a macOS development environment provisioning CLI built with Python and Ansible.

## Source Layout (`src/menv/`)

- **commands/**: Contains Typer-based CLI command definitions.
  - `config.py`, `create.py`, `make.py`, `switch.py`, `update.py`
- **models/**: Contains data models.
  - Currently uses `TypedDict` for configuration (`MenvConfig`, `VcsIdentityConfig`) instead of validated classes.
- **services/**: Contains the core business logic.
  - `ansible_runner.py`: Wraps `ansible-playbook` execution.
  - `config_storage.py`: Manages configuration persistence (TOML).
  - `config_deployer.py`: Handles copying role configs to user directory.
  - `version_checker.py`: Checks for updates via GitHub API.
  - `ansible_paths.py`: Resolves paths to bundled Ansible resources.
  - `playbook.py`: Parses `playbook.yml`.
- **protocols/**: Defines abstract base classes (Protocols) for services to enable testing and loose coupling.
- **ansible/**: Contains the bundled Ansible playbooks, roles, and configuration.

## Key Observations

- **Dependency Management**: Uses `uv` for dependency management.
- **CLI Framework**: Uses `typer` for the command-line interface.
- **Configuration**: Uses TOML format (`tomllib` for reading).
- **Execution**: Delegates to `ansible-playbook` via `subprocess`.
