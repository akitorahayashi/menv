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

## Phantom Terms
*   `introduce`: Referenced in documentation but does not exist.
