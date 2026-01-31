# Vocabulary and Terminology

## Conflicts

### Config
*   **Concept 1:** User Identity (Name, Email).
    *   *Managed by:* `ConfigStorage`.
    *   *CLI:* `menv config set`, `menv config show`.
*   **Concept 2:** Role Configuration (Ansible Variables).
    *   *Managed by:* `ConfigDeployer`.
    *   *CLI:* `menv config create`.
*   **Status:** **Ambiguous**. One term maps to two distinct concepts.

### Create
*   **Concept 1:** Provision Environment.
    *   *CLI:* `menv create`.
*   **Concept 2:** Deploy Configuration Files.
    *   *CLI:* `menv config create`.
    *   *Internal Term:* `deploy`.
*   **Status:** **Ambiguous**. "Create" is overloaded.

### Make vs Run
*   **Concept:** Execute a task/tag.
*   **CLI:** `make`.
*   **Internal Term:** `run` (`AnsibleRunner.run_playbook`).
*   **Status:** **Inconsistent**.

### System
*   **Concept 1:** macOS Defaults/Preferences.
    *   *Managed by:* `roles/system`.
*   **Concept 2:** General Unix Utilities.
    *   *Managed by:* `roles/shell/config/common/alias/system/macos.sh`.
*   **Status:** **Overloaded**. "System" is used for both OS preferences and basic shell tools.

### Apple vs MacOS
*   **Concept 1:** Development Tools (Xcode, Swift).
    *   *Term:* `Apple` (`alias/apple.sh`).
*   **Concept 2:** System/Unix Utilities.
    *   *Term:* `MacOS` (`alias/system/macos.sh`).
*   **Status:** **Vague**. "Apple" and "MacOS" are overlapping terms used for distinct but adjacent categories.

## Phantom Terms
*   `introduce`: Referenced in documentation but does not exist.
