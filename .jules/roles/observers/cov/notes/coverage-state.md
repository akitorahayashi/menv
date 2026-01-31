# Coverage State

## Status: Critical Gaps
As of the latest observation, the project **lacks all coverage infrastructure**.

### Configuration
- `pyproject.toml`: No coverage settings.
- `justfile`: No coverage recipes.
- Dependencies: `pytest-cov` and `coverage` are missing.

### Risks
- **Blindness**: No visibility into which lines of code are executed by tests.
- **Regression**: New code can be added without tests and go unnoticed.
- **Critical Paths**: Core logic like `AnsibleRunner` error handling is likely uncovered by unit tests and relies solely on happy-path integration tests.

### Targets
- No targets defined (e.g., Line %, Branch %).
