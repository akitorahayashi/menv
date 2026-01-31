# Project Structure and Naming Conventions

## Commands
*   **Location:** `src/menv/commands/`
*   **Convention:** One command per file (e.g., `create.py` for `menv create`).
*   **Violations:**
    *   `list` command is implemented in `make.py` as `list_tags`.

## Services
*   **Location:** `src/menv/services/`
*   **Convention:** One class per file, matching the service name (e.g., `config_storage.py` -> `ConfigStorage`).
*   **Violations:**
    *   `PlaybookService` in `playbook.py` (filename mismatch).
    *   `PlaybookService` uses generic "Service" suffix unlike other domain services.

## Protocols
*   **Location:** `src/menv/protocols/`
*   **Convention:** `XxxProtocol` suffix.
*   **Status:** Consistent.

## Models
*   **Location:** `src/menv/models/`
*   **Status:** Consistent.
