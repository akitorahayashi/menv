# Project Structure Analysis

## Service Layer (`src/menv/services/`)
- Adheres to Protocol/Implementation pattern (`Protocol` suffix in `src/menv/protocols/`).
- Anti-patterns identified:
  - `AnsiblePaths`: Unsafe resource cleanup (`__del__` with `except Exception: pass`).
  - `VersionChecker`: Swallowed exceptions hiding failures.
  - `ConfigStorage`: Fragile manual TOML serialization.
  - `AnsibleRunner`: I/O mixing (direct `sys.stdout` and `subprocess`).

## Commands (`src/menv/commands/`)
- Uses `Typer` for CLI.
- Dependency injection via `AppContext`.
- Architecture violation: `list` command logic resides in `make.py`.
- Boundary issue: `TypedDict` (`MenvConfig`) used without runtime validation at IO boundary.

## Models (`src/menv/models/`)
- `TypedDict` usage provides type hints but no runtime safety for external data (config files).
