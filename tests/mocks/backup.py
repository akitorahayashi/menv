"""Mock backup services for testing."""

from __future__ import annotations

from pathlib import Path


class MockSystemBackupService:
    """Mock system backup service."""

    def backup(
        self,
        config_dir: Path,
        definitions_dir: Path | None = None,
        output: Path | None = None,
    ) -> int:
        """Execute the system defaults backup."""
        return 0


class MockVSCodeBackupService:
    """Mock VSCode backup service."""

    def backup(self, config_dir: Path, output: Path | None = None) -> int:
        """Execute the VSCode extensions backup."""
        return 0
