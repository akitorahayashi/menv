# Project Structure and Testing Strategy

## File Layout
- **Source**: `src/menv/`
  - `commands/`: CLI command implementations.
  - `services/`: Core logic and business rules.
  - `models/`: Data structures.
  - `protocols/`: Interfaces.
  - `ansible/`: Bundled Ansible roles.
- **Tests**: `tests/`
  - `unit/`: Isolated tests for commands and services, using mocks.
  - `intg/`: Integration tests, primarily for Ansible roles.
  - `mocks/`: Shared mock implementations.

## Testing Strategy
- **Unit Tests**: Focus on logic verification using `pytest` and mocks.
- **Integration Tests**: Verify Ansible role execution and interactions.
- **Execution**: Run via `just test` (calls `pytest`).

## Observations
- 1:1 mapping between `src/menv/commands` and `tests/unit/commands`.
- Service tests are mostly present but `AnsibleRunner` is a notable gap in unit tests.
