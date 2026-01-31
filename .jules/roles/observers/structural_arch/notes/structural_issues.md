# Structural Issues

## CLI Command Structure
- **Violation:** The `list` command is implemented as `list_tags` inside `src/menv/commands/make.py`.
- **Constraint:** One command per file.
- **Impact:** Reduces findability and cohesion. The command should be moved to `src/menv/commands/list.py`.

## Hidden Application Logic
- **Violation:** Significant application logic resides in `src/menv/ansible/scripts/`.
- **Examples:**
  - `src/menv/ansible/scripts/shell/aider.py`: A full CLI wrapper for `aider` using `ollama`.
  - `src/menv/ansible/scripts/system/backup-system.py`: Core backup logic for macOS defaults.
- **Impact:** Logic is disconnected from the main application, making it hard to find, test, and maintain. It creates "entangled I/O" where business logic is mixed with scripts.

## Validated Structure
The following structure has been validated and generally adheres to the architecture:
- `src/menv/commands/`: CLI commands (except `list`).
- `src/menv/services/`: Business logic services.
- `src/menv/protocols/`: Protocol definitions for services.
- `src/menv/models/`: Data models.
- `src/menv/ansible/roles/`: Ansible roles structure.
