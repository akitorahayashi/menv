"""Protocols for backup services."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class SystemBackupProtocol(Protocol):
    """Protocol for system backup service."""

    def backup(
        self,
        config_dir: Path,
        definitions_dir: Path | None = None,
        output: Path | None = None,
    ) -> int:
        """Execute the system defaults backup."""
        ...


class VSCodeBackupProtocol(Protocol):
    """Protocol for VSCode backup service."""

    def backup(self, config_dir: Path, output: Path | None = None) -> int:
        """Execute the VSCode extensions backup."""
        ...
