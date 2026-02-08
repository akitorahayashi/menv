"""Tests for VSCode backup service."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from menv.services.backup.vscode import VSCodeBackupService


class TestVSCodeBackupService:
    @patch("menv.services.backup.vscode.shutil.which")
    @patch("menv.services.backup.vscode.subprocess.run")
    def test_backup_success(self, mock_run, mock_which, tmp_path):
        service = VSCodeBackupService()
        config_dir = tmp_path / "config"
        config_dir.mkdir()

        mock_which.return_value = "/usr/bin/code"
        mock_run.return_value.stdout = "ext1\next2"
        mock_run.return_value.returncode = 0

        output = tmp_path / "vscode.json"

        assert service.backup(config_dir, output=output) == 0

        assert output.exists()
        content = output.read_text()
        assert '"extensions": [' in content
        assert '"ext1",' in content
        assert '"ext2"' in content

    @patch("menv.services.backup.vscode.shutil.which")
    def test_backup_command_not_found(self, mock_which, tmp_path):
        service = VSCodeBackupService()
        config_dir = tmp_path / "config"

        mock_which.return_value = None
        # Also ensure hardcoded paths don't exist
        with patch("menv.services.backup.vscode.Path.exists", return_value=False):
            assert service.backup(config_dir) == 1

    @patch("menv.services.backup.vscode.shutil.which")
    @patch("menv.services.backup.vscode.subprocess.run")
    def test_backup_timeout(self, mock_run, mock_which, tmp_path):
        service = VSCodeBackupService()
        config_dir = tmp_path / "config"
        mock_which.return_value = "code"

        mock_run.side_effect = subprocess.TimeoutExpired(["code"], 10)

        assert service.backup(config_dir) == 1

    @patch("menv.services.backup.vscode.shutil.which")
    @patch("menv.services.backup.vscode.subprocess.run")
    def test_backup_subprocess_error(self, mock_run, mock_which, tmp_path):
        service = VSCodeBackupService()
        config_dir = tmp_path / "config"
        mock_which.return_value = "code"

        mock_run.side_effect = subprocess.CalledProcessError(1, ["code"])

        assert service.backup(config_dir) == 1
