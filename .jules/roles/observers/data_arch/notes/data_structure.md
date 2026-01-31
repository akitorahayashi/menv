# Data Architecture State

## Configuration Management

### Single Source of Truth (SSOT)
- **User Config Path**: The user configuration directory (`~/.config/menv`) is currently not centralized. It is hardcoded in:
  - `src/menv/services/config_storage.py` (Default parameter)
  - `src/menv/services/ansible_runner.py` (Explicit path construction)
- **Ansible Role Config**: Role configurations reside in `~/.config/menv/roles/`, but this structure is only implicitly defined by the `AnsibleRunner` passing a path to `ansible-playbook`.

### Data Models
- **MenvConfig**: Defined as a `TypedDict` in `src/menv/models/config.py`.
- **Validation**:
  - **Python**: No runtime validation. `ConfigStorage` loads data with defaults (`.get()`), potentially masking corruption or missing fields.
  - **Ansible**: No validation. Ansible tasks blindly load YAML files via `include_vars`.

### Persistence
- **Serialization**: `ConfigStorage.save` manually constructs TOML strings. This is a fragile anti-pattern that risks generating invalid TOML or mishandling escaping.

## Data Flow

1. **CLI -> Python Services**: Commands verify arguments (via Typer) but rely on `ConfigStorage` for state.
2. **Python Services -> Ansible**:
   - `AnsibleRunner` constructs a `subprocess` call to `ansible-playbook`.
   - **Coupling**: It passes `local_config_root` as an extra var (`-e`).
   - **Implicit Contract**: Ansible tasks assume the internal structure of `local_config_root` (e.g., `<role>/common/models.yml`) without any contract enforcement in the Python layer.
