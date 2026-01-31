# Project Structure Observations

## CLI Command Structure
- **Pattern**: `src/menv/commands/<command>.py`.
- **Constraint**: `AGENTS.md` requires "1 command per file".
- **Status**: Mostly followed (backup, config, create, make, switch, update).
- **Exceptions**: The `list` command is implemented within `src/menv/commands/make.py`.

## Command Functionality Issues
- **Backup**: Broken implementation. `menv backup` fails to pass required arguments (`config_dir`) to backend scripts.
- **Introduce**: Missing implementation. Documented in `README.md` but does not exist in codebase.
- **List**: Documentation error. Docstrings in `src/menv/commands/make.py` incorrectly reference `menv make list` instead of `menv list`.

## Ansible Role Configuration
- **Pattern**: `src/menv/ansible/roles/<role>/config/{common,profiles}/`.
- **Constraint**: Documentation claims only `brew` role uses `profiles`.
- **Status**: Contradicted by implementation.
- **Exceptions**: `llm` role utilizes `config/profiles/mac-mini/models.yml`.

## Role Implementation
- **Roles**: brew, editor, gh, go, llm, nodejs, python, ruby, rust, shell, ssh, system, vcs.
- **Node.js**: Includes `coder` task.
- **Rust**: Uses `tools.yml` to define GitHub release downloads.
