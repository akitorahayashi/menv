"""Tests for backup command execution."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from typer.testing import CliRunner

from menv.context import AppContext
from menv.main import app


class TestBackupExecution:
    """Tests for the backup command execution."""

    def test_backup_system_calls_service(self, cli_runner: CliRunner) -> None:
        """Test that backup system calls the system service backup function."""
        mock_ctx = MagicMock(spec=AppContext)
        mock_system_backup = MagicMock()
        mock_system_backup.backup.return_value = 0
        mock_ctx.system_backup = mock_system_backup

        mock_config_deployer = MagicMock()
        mock_config_deployer.get_local_config_path.return_value = Path("/tmp/local")
        mock_config_deployer.get_package_config_path.return_value = Path("/tmp/package")
        mock_ctx.config_deployer = mock_config_deployer

        result = cli_runner.invoke(app, ["backup", "system"], obj=mock_ctx)

        assert result.exit_code == 0
        mock_system_backup.backup.assert_called_once()
        kwargs = mock_system_backup.backup.call_args.kwargs
        assert "common" in str(kwargs["config_dir"])

    def test_backup_vscode_calls_service(self, cli_runner: CliRunner) -> None:
        """Test that backup vscode calls the vscode extensions service."""
        mock_ctx = MagicMock(spec=AppContext)
        mock_vscode_backup = MagicMock()
        mock_vscode_backup.backup.return_value = 0
        mock_ctx.vscode_backup = mock_vscode_backup

        mock_config_deployer = MagicMock()
        mock_config_deployer.get_local_config_path.return_value = Path("/tmp/local")
        mock_ctx.config_deployer = mock_config_deployer

        result = cli_runner.invoke(app, ["backup", "vscode"], obj=mock_ctx)

        assert result.exit_code == 0
        mock_vscode_backup.backup.assert_called_once()
