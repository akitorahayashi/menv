# Data Architecture Overview

## Configuration Management

The application manages two types of configuration:
1.  **User Configuration**: Stored in `~/.config/menv/config.toml` (identity settings).
2.  **Role Configuration**: Stored in `~/.config/menv/roles/` (Ansible role configs).

### Models
-   `MenvConfig` and `VcsIdentityConfig` (TypedDict) define the user configuration structure.
-   No formal model exists for role configurations (they are directory-based).

### Storage
-   `ConfigStorage` handles loading/saving user configuration using TOML.
-   Manual TOML string construction is used for saving (no library).

### Ansible Integration
-   `AnsibleRunner` executes playbooks, passing configuration paths as extra vars.
-   `PlaybookService` acts as the SSOT for playbook structure (tags/roles), derived from parsing `playbook.yml`.

## Observed Issues

1.  **SSOT Violation**: The path `~/.config/menv` is hardcoded in multiple services (`ConfigStorage`, `AnsibleRunner`, `ConfigDeployer`).
2.  **Fragile Transformation**: Manual TOML serialization in `ConfigStorage.save`.
3.  **Missing Validation**: Lack of strict schema validation for user configuration.
