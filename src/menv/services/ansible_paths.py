"""Path resolution for package-internal Ansible resources."""

from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path

from menv.protocols.ansible_paths import AnsiblePathsProtocol


class AnsiblePaths(AnsiblePathsProtocol):
    """Resolve package-internal Ansible paths."""

    def __init__(self) -> None:
        self._ansible_dir: Path | None = None

    def ansible_dir(self) -> Path:
        """Get the path to the ansible directory within the package."""
        if self._ansible_dir is not None:
            return self._ansible_dir

        source = files("menv").joinpath("ansible")
        with as_file(source) as ansible_path:
            self._ansible_dir = Path(ansible_path)

        assert self._ansible_dir is not None
        return self._ansible_dir

    def playbook_path(self) -> Path:
        """Get the path to the main playbook.yml file."""
        return self.ansible_dir() / "playbook.yml"

    def ansible_config_path(self) -> Path:
        """Get the path to ansible.cfg configuration file."""
        return self.ansible_dir() / "ansible.cfg"
