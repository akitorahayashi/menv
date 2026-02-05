"""Integration test for Ansible playbook syntax."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


class TestPlaybookSyntax:
    """Validate Ansible playbook syntax using ansible-playbook."""

    def test_playbook_syntax_check(self, project_root: Path) -> None:
        """Run ansible-playbook --syntax-check on the main playbook."""
        playbook_path = project_root / "src" / "menv" / "ansible" / "playbook.yml"

        assert playbook_path.exists(), f"Playbook not found at {playbook_path}"

        # We need to set ANSIBLE_CONFIG to ensure roles path is correct?
        # The project uses local ansible.cfg in src/menv/ansible/ansible.cfg
        ansible_dir = playbook_path.parent
        ansible_cfg = ansible_dir / "ansible.cfg"

        cmd = [
            "ansible-playbook",
            str(playbook_path),
            "--syntax-check",
        ]

        # Ensure we run in the ansible dir so relative paths in ansible.cfg work
        # OR set ANSIBLE_CONFIG env var
        import os
        env = os.environ.copy()
        env["ANSIBLE_CONFIG"] = str(ansible_cfg)

        # We might need to pass extra vars if they are required for syntax check?
        # Syntax check usually doesn't evaluate vars but might fail if imports depend on vars.
        # menv playbook uses:
        # roles:
        #   - { role: brew, tags: ["brew-formulae", "brew-cask"] }
        # No dynamic includes that depend on vars in the top level.

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                env=env,
                cwd=str(ansible_dir), # Running from ansible dir is safer for role resolution
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Playbook syntax check failed:\n{e.stdout}\n{e.stderr}")

        assert result.returncode == 0
