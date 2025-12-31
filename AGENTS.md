# menv - macOS Environment Setup Project

## Overview

pipx-installable CLI for macOS dev environment setup using bundled Ansible playbooks.

## CLI Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `menv introduce <profile>` | `itr` | Interactive setup guide (macbook/mbk, mac-mini/mmn) |
| `menv make <tag> [profile]` | `mk` | Run individual task (default: common) |
| `menv list` | `ls` | List available tags |
| `menv backup <target>` | `bk` | Backup system/vscode |
| `menv config <action>` | `cf` | Manage VCS identities (set/show) |
| `menv switch <profile>` | `sw` | Switch VCS identity (personal/p, work/w) |
| `menv code` | - | Clone ~/menv (if needed) and open in VS Code |
| `menv update` | `u` | Self-update via pipx |

## Package Structure

```
src/menv/
├── main.py           # Typer CLI entry point
├── context.py        # AppContext (DI container)
├── commands/         # CLI commands (1 command per file)
├── models/           # Data models (1 file per domain)
├── services/         # Service classes (1 class per file)
├── protocols/        # Protocol definitions (1 per service)
└── ansible/          # Bundled Ansible playbooks and roles

tests/
├── mocks/            # Mock implementations (1 class per file, Protocol-compliant)
```

## Architecture Principles

### Directory Naming
- **No ambiguous names**: `core/`, `utils/`, `helpers/` are forbidden
- Every file must belong to a clear, specific category

### Services (`services/`)
- **1 class per file**
- Each service must have a corresponding Protocol in `protocols/`
- Example: `services/config_storage.py` ↔ `protocols/config_storage.py`

### Models (`models/`)
- **1 file per domain** (group related models)
- Pure data structures (dataclass, TypedDict)
- No business logic

### Protocols (`protocols/`)
- Define interface for each service
- Both real implementations and mocks must satisfy the Protocol

### Mocks (`tests/mocks/`)
- **1 class per file** (mirror service structure)
- Must implement corresponding Protocol
- Never put implementations in `__init__.py`

## Design Rules

### Path Resolution
- CLI passes `profile`, `config_dir_abs_path`, `repo_root_path` as Ansible extra vars
- Roles handle fallback logic (profile-specific → common)
- Use `importlib.resources` for package path resolution

### Symlink Enforcement
- Always use `force: true` when creating symlinks
- Overwrite existing files/links unconditionally

### Testing
- Run via `just test`
- Mocks must be Protocol-compliant for type safety
- Prefer DI over monkeypatch where possible

### Development
- `just run <args>`: Run menv in dev mode
- `just check`: Format and lint
