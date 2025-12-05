# Comprehensive Update Plan: Xcode Settings Codification & Application Feature

## 1. Strategic Overview

  * **Role Placement:** Add a dedicated area for Xcode in `ansible/roles/editor`.
  * **Design Philosophy:** **"Category-based Configuration"**.
      * Manage configuration files as separate YAML files by functional category.
      * **Configuration as Documentation:** Write a one-line comment above each setting describing its purpose.
  * **Application Flow:** Ansible tasks dynamically load all YAML definition files in the specified directory and apply them in bulk.

## 2. Directory Structure and File Layout

```text
ansible/roles/editor/
├── config/
│   └── common/
│       ├── xcode/                  <-- (Add: Xcode-specific settings location)
│       │   ├── editor.yml          # Editor display/editing
│       │   ├── build.yml           # Build, performance, debugging
│       │   ├── ui.yml              # UI, appearance, menus
│       │   └── behavior.yml        # Input behavior, usability
│       ├── cursor-extensions.json
│       └── settings.json           <-- (Existing: For VS Code)
├── tasks/
│   ├── main.yml                    # Entry point (modify)
│   ├── cursor.yml
│   ├── vscode.yml
│   ├── xcode.yml                   <-- (Add: defaults application logic)
│   └── apply_xcode_defaults.yml    <-- (Add: internal task)
└── tasks.just                       # Standalone execution (modify)
```

## 3. Implementation Tasks

### A. Configuration Files
Create the following YAML files in `ansible/roles/editor/config/common/xcode/`:

1.  **`editor.yml`**
    *   Line numbers, indentation (spaces, width 4), trimming whitespace, page guide (120), folding sidebar.
2.  **`build.yml`**
    *   Build duration, numeric indexer progress.
3.  **`ui.yml`**
    *   Dock icon version number, debug menu.
4.  **`behavior.yml`**
    *   Disable accent menu (key hold), enable multi-cursor, disable state restoration.

### B. Logic Implementation
1.  **`ansible/roles/editor/tasks/xcode.yml`**
    *   Kill Xcode.
    *   Load definition files using `fileglob`.
    *   Loop through definitions and include `apply_xcode_defaults.yml`.
2.  **`ansible/roles/editor/tasks/apply_xcode_defaults.yml`**
    *   Apply settings using `community.general.osx_defaults`.

### C. Entry Point & Justfile
1.  **`ansible/roles/editor/tasks/main.yml`**
    *   Add `include_tasks: xcode.yml` with `tags: xcode`.
2.  **`ansible/roles/editor/tasks.just`**
    *   Add `setup-xcode` command.

## 4. Documentation Strategy

*   **`README.md`**: Update the "Editor Configuration" section to explicitly mention Xcode support and how to use it (e.g., `just setup-xcode` or via `make macbook` if integrated later, though for now it's part of the editor role which is in `make macbook`).
    *   Note: The editor role is included in `common` or via tags. The user can run `just setup-editor` or `just setup-xcode`.

## 5. Test Strategy

*   **New Test File**: `tests/config/editor/test_xcode_config_files.py`
    *   **Syntax Check**: Verify valid YAML syntax.
    *   **Schema Check**: Verify each item has `key`, `type`, `value`, `domain`.
    *   **Type Validation**: Ensure `type` is one of `bool`, `int`, `string`, `float`.

## 6. Verification Steps

1.  Run `just test` to execute the new test and ensure existing tests pass.
2.  Inspect created files to ensure correct content.
