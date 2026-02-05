"""Tests for update command."""

from __future__ import annotations

from unittest.mock import Mock

from typer.testing import CliRunner

from menv.context import AppContext
from menv.main import app


class TestUpdateCommand:
    """Tests for the update command."""

    def test_update_help_shows_description(self, cli_runner: CliRunner) -> None:
        """Test that update --help shows description."""
        result = cli_runner.invoke(app, ["update", "--help"])

        assert result.exit_code == 0
        assert "update" in result.output.lower() or "version" in result.output.lower()

    def test_update_already_latest(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test update when already on latest version."""
        checker = mock_app_context.version_checker
        # Patch methods on the mock instance
        checker.get_current_version = Mock(return_value="1.0.0")
        checker.get_latest_version = Mock(return_value="1.0.0")
        checker.needs_update = Mock(return_value=False)

        result = cli_runner.invoke(app, ["update"])

        assert result.exit_code == 0
        assert "You are already on the latest version" in result.output

    def test_update_available_success(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test successful update when available."""
        checker = mock_app_context.version_checker
        checker.get_current_version = Mock(return_value="1.0.0")
        checker.get_latest_version = Mock(return_value="2.0.0")
        checker.needs_update = Mock(return_value=True)
        checker.run_pipx_upgrade = Mock(return_value=0)

        result = cli_runner.invoke(app, ["update"])

        assert result.exit_code == 0
        assert "Update available: 1.0.0 → 2.0.0" in result.output
        assert "Successfully updated" in result.output

        checker.run_pipx_upgrade.assert_called_once()

    def test_update_available_failure(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test update failure."""
        checker = mock_app_context.version_checker
        checker.get_current_version = Mock(return_value="1.0.0")
        checker.get_latest_version = Mock(return_value="2.0.0")
        checker.needs_update = Mock(return_value=True)
        checker.run_pipx_upgrade = Mock(return_value=1)

        result = cli_runner.invoke(app, ["update"])

        assert result.exit_code == 1
        assert "Update failed with exit code 1" in result.output

    def test_update_network_error(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test network error fetching latest version."""
        checker = mock_app_context.version_checker
        checker.get_current_version = Mock(return_value="1.0.0")
        checker.get_latest_version = Mock(return_value=None)

        result = cli_runner.invoke(app, ["update"])

        assert result.exit_code == 1
        assert "Could not fetch latest version" in result.output
