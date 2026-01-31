# Structural Issues

## CLI Command Structure
- **Violation:** The `list` command is implemented as `list_tags` inside `src/menv/commands/make.py`.
- **Constraint:** One command per file.
- **Impact:** Reduces findability and cohesion. The command should be moved to `src/menv/commands/list.py`.

## Business Logic Leak in Make Command
- **Violation:** The `make` command (`src/menv/commands/make.py`) contains hardcoded business logic.
- **Examples:**
  - `TAG_GROUPS`: Hardcoded dictionary mapping tags to groups.
  - `VALID_PROFILES`: Hardcoded set of valid profiles.
- **Constraint:** Separation of Concerns (Business logic in Services/Models).
- **Impact:** Logic is coupled to the CLI interface, making it hard to reuse or test independently.

## Hidden Application Logic (Entangled I/O)
- **Violation:** Significant application logic resides in `src/menv/ansible/scripts/` instead of the main application.
- **Examples:**
  - `src/menv/ansible/scripts/shell/aider.py`: A full CLI wrapper for `aider` using `ollama`.
  - `src/menv/ansible/scripts/system/backup-system.py`: Core backup logic for macOS defaults.
  - `src/menv/ansible/scripts/editor/backup-extensions.py`: Backup logic for VSCode extensions.
- **Impact:** Logic is disconnected from the main application (`src/menv/`), making it hard to find, test, and maintain. It creates "entangled I/O" where business logic is mixed with scripts.

## Validated Structure
The following structure has been validated and generally adheres to the architecture:
- `src/menv/commands/`: CLI commands (except `list` and `make` logic leak).
- `src/menv/services/`: Business logic services (1 class per file).
- `src/menv/protocols/`: Protocol definitions for services (Matches services perfectly).
- `src/menv/models/`: Data models.
- `src/menv/ansible/roles/`: Ansible roles structure.
