# Architecture and Conventions

## Project Structure
- **Ansible Root:** `src/menv/ansible/` contains the Ansible playbooks and roles.
- **Config Root:** Roles store configuration in `src/menv/ansible/roles/<role>/config/`.
- **Profiles:** While docs state only `brew` uses profiles, `llm` also uses `config/profiles/` (e.g., `mac-mini`).

## Tooling
- **Primary CLI:** `menv` (Python/Typer app) is the primary entry point.
- **Development:** `justfile` handles development tasks (`just test`, `just check`).
- **Legacy:** `Makefile` is not present in the current codebase.

## LLM Context Management
- **Local Context:** `cld-ln` (defined in `roles/shell/.../llm.sh`) links the repository root `AGENTS.md` to `.claude/CLAUDE.md`. It explicitly checks for `AGENTS.md` existence.
- **Global Context:** `cpt-ln` (defined in `roles/shell/.../coder.sh`) links a global `AGENTS.md` from `~/.config/menv/...` to `.github/copilot-instructions.md`. It does *not* strictly require a local `AGENTS.md`.
