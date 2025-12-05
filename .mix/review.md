setup-xcodeではなくjust xcodeというレシピ名にしてください


ansible/roles/editor/tasks/xcode.yml
Comment on lines +2 to +5
- name: Ensure Xcode is not running (prevent defaults caching issues)
  ansible.builtin.shell: pkill Xcode || true
  changed_when: false
  tags: always
@gemini-code-assist
gemini-code-assist bot
6 minutes ago
high

Using ansible.builtin.shell with || true can hide real errors from pkill. For instance, a syntax error in the command would be ignored. It's more robust to use ansible.builtin.command and check for specific successful exit codes. pkill returns 1 when no processes are found, and >1 for actual errors. This change makes the task fail on unexpected errors while still succeeding if Xcode is not running.

I recommend replacing this task with:

- name: Ensure Xcode is not running (prevent defaults caching issues)
  ansible.builtin.command: pkill Xcode
  register: pkill_result
  changed_when: false
  failed_when: "pkill_result.rc > 1"
  tags: always
@akitorahayashi	Reply...
.mix/revised_tasks.md
## 4. Documentation Strategy

*   **`README.md`**: Update the "Editor Configuration" section to explicitly mention Xcode support and how to use it (e.g., `just setup-xcode` or via `make macbook` if integrated later, though for now it's part of the editor role which is in `make macbook`).
    *   Note: The editor role is included in `common` or via tags. The user can run `just setup-editor` or `just setup-xcode`.
@gemini-code-assist
gemini-code-assist bot
6 minutes ago
medium

The documentation mentions a just setup-editor command, but this command is not defined in the ansible/roles/editor/tasks.just file. The available commands are vscode, cursor, and the newly added setup-xcode. To avoid confusion, you might want to update this note to reflect the actual available commands or add the setup-editor command if it's intended to be a new alias.

@akitorahayashi	Reply...
ansible/roles/editor/tasks/xcode.yml
Comment on lines +7 to +15
- name: Load all Xcode definition files
  ansible.builtin.set_fact:
    xcode_definitions: "{{ lookup('fileglob', role_path + '/config/common/xcode/*.yml', wantlist=True) }}"

- name: Apply Xcode preferences from definitions
  include_tasks: apply_xcode_defaults.yml
  loop: "{{ xcode_definitions }}"
  loop_control:
    loop_var: definition_file
@gemini-code-assist
gemini-code-assist bot
6 minutes ago
medium

The current implementation uses include_tasks within a loop, which has some performance overhead. A more efficient and modern approach in Ansible is to first aggregate all settings from the YAML files into a single list and then run one osx_defaults task that loops over this combined list. This simplifies the logic by removing the need for apply_xcode_defaults.yml.

You could replace lines 7-15 in this file and delete ansible/roles/editor/tasks/apply_xcode_defaults.yml with the following tasks in xcode.yml:

- name: Load and combine all Xcode definitions
  ansible.builtin.set_fact:
    xcode_settings: "{{ xcode_settings | default([]) + (lookup('file', item) | from_yaml) }}"
  loop: "{{ lookup('fileglob', role_path + '/config/common/xcode/*.yml', wantlist=True) }}"

- name: Apply all Xcode preferences
  community.general.osx_defaults:
    domain: "{{ item.domain }}"
    key: "{{ item.key }}"
    type: "{{ item.type }}"
    value: "{{ item.value }}"
    state: present
  loop: "{{ xcode_settings | default([]) }}"
@akitorahayashi	Reply...
tests/config/editor/test_xcode_config_files.py
Comment on lines +15 to +31
@pytest.fixture(scope="session")
def xcode_yml_files(xcode_config_path: Path) -> list[str]:
    """Discover all .yml files in the Xcode config directory."""
    return glob.glob(os.path.join(xcode_config_path, "*.yml"))


class TestXcodeConfigs:
    def test_xcode_definitions(self, xcode_yml_files: list[str]) -> None:
        """
        Verify syntax and schema for all Xcode definition .yml files.
        """
        if not xcode_yml_files:
            pytest.fail("No Xcode .yml config files found to test.")

        for yaml_file_path in xcode_yml_files:
            file_basename = os.path.basename(yaml_file_path)
            with open(yaml_file_path, "r") as f:
@gemini-code-assist
gemini-code-assist bot
6 minutes ago
medium

This is a great set of tests for the new configuration files. To improve the code and make it more consistent with modern Python practices, I suggest using pathlib throughout. The xcode_yml_files fixture can be simplified to use Path.glob(), and the test function can then operate on Path objects directly, which cleans up the file handling code. This also allows removing the glob and os imports.

Here's how you could refactor this part of the file:

@pytest.fixture(scope="session")
def xcode_yml_files(xcode_config_path: Path) -> list[Path]:
    """Discover all .yml files in the Xcode config directory."""
    return list(xcode_config_path.glob("*.yml"))


class TestXcodeConfigs:
    def test_xcode_definitions(self, xcode_yml_files: list[Path]) -> None:
        """
        Verify syntax and schema for all Xcode definition .yml files.
        """
        if not xcode_yml_files:
            pytest.fail("No Xcode .yml config files found to test.")

        for yaml_file_path in xcode_yml_files:
            file_basename = yaml_file_path.name
            with yaml_file_path.open("r") as f:
@akitorahayashi	Reply...
coderabbitai[bot]
coderabbitai bot reviewed 4 minutes ago
coderabbitai bot
left a comment
Actionable comments posted: 1

🧹 Nitpick comments (3)
📜 Review details
ansible/roles/editor/tasks.just
Comment on lines +13 to +15
# Setup Xcode configuration only
setup-xcode:
    ansible-playbook {{ playbook_dir }}/playbook.yml --tags xcode
@coderabbitai
coderabbitai bot
4 minutes ago
⚠️ Potential issue | 🔴 Critical

Fix undefined variable causing pipeline failure.

The playbook_dir variable is not defined, causing the pipeline to fail. Additionally, this target is inconsistent with the existing vscode and cursor targets which use the _run_ansible helper function imported from ../../ansible.just.

Apply this diff to fix the issue and maintain consistency:

 # Setup Xcode configuration only
 setup-xcode:
-    ansible-playbook {{ playbook_dir }}/playbook.yml --tags xcode
+  @echo "🚀 Running common Xcode setup..."
+  @just _run_ansible "editor" "common" "xcode"