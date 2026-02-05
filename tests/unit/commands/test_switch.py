"""Tests for switch command."""

from __future__ import annotations

import subprocess
from typing import cast
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from menv.context import AppContext
from menv.main import app


class TestSwitchCommand:
    """Tests for the switch command."""

    def test_switch_help_shows_profile_argument(self, cli_runner: CliRunner) -> None:
        """Test that switch --help shows profile argument."""
        result = cli_runner.invoke(app, ["switch", "--help"])

        assert result.exit_code == 0
        assert "PROFILE" in result.output or "profile" in result.output.lower()

    @patch("menv.commands.switch.run_git_config")
    @patch("menv.commands.switch.run_jj_config")
    @patch("menv.commands.switch.get_current_git_user")
    def test_switch_personal_success(
        self,
        mock_get_user: Mock,
        mock_jj: Mock,
        mock_git: Mock,
        cli_runner: CliRunner,
        mock_app_context: AppContext,
    ) -> None:
        """Test successful switch to personal profile."""
        # Setup config storage
        mock_storage = cast(Mock, mock_app_context.config_storage)
        # Assign Mock objects to overrides methods
        mock_storage.exists = Mock(return_value=True)
        mock_storage.get_identity = Mock(return_value={
            "name": "John Doe",
            "email": "john@example.com",
        })

        mock_git.return_value = True
        mock_jj.return_value = True
        mock_get_user.return_value = ("John Doe", "john@example.com")

        result = cli_runner.invoke(app, ["switch", "personal"])

        assert result.exit_code == 0
        assert "Switching to personal identity" in result.output
        assert "Switched to personal identity" in result.output
        assert "Name:  John Doe" in result.output

        # Verify calls
        assert mock_git.call_count == 2
        mock_git.assert_any_call("user.name", "John Doe")
        mock_git.assert_any_call("user.email", "john@example.com")

        assert mock_jj.call_count == 2

    def test_switch_fails_if_no_config(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test switch fails if config storage does not exist."""
        mock_storage = cast(Mock, mock_app_context.config_storage)
        mock_storage.exists = Mock(return_value=False)

        result = cli_runner.invoke(app, ["switch", "personal"])

        assert result.exit_code == 1
        assert "No configuration found" in result.output

    def test_switch_fails_invalid_profile(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test switch fails with invalid profile."""
        mock_storage = cast(Mock, mock_app_context.config_storage)
        mock_storage.exists = Mock(return_value=True)

        result = cli_runner.invoke(app, ["switch", "invalid"])

        assert result.exit_code == 1
        assert "Invalid profile" in result.output

    @patch("menv.commands.switch.run_git_config")
    def test_switch_fails_git_config(
        self,
        mock_git: Mock,
        cli_runner: CliRunner,
        mock_app_context: AppContext,
    ) -> None:
        """Test switch fails if git config fails."""
        mock_storage = cast(Mock, mock_app_context.config_storage)
        mock_storage.exists = Mock(return_value=True)
        mock_storage.get_identity = Mock(return_value={
            "name": "John",
            "email": "john@example.com",
        })

        # Git config fails
        mock_git.return_value = False

        result = cli_runner.invoke(app, ["switch", "work"])

        assert result.exit_code == 1
        assert "Failed to set Git configuration" in result.output

    def test_switch_aliases(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test aliases (p -> personal)."""
        mock_storage = cast(Mock, mock_app_context.config_storage)
        mock_storage.exists = Mock(return_value=True)
        mock_storage.get_identity = Mock(return_value={"name": "J", "email": "j@e.c"})

        with patch("menv.commands.switch.run_git_config") as mock_git, \
             patch("menv.commands.switch.run_jj_config") as mock_jj, \
             patch("menv.commands.switch.get_current_git_user") as mock_user:

             mock_git.return_value = True
             mock_jj.return_value = True
             mock_user.return_value = ("J", "j@e.c")

             result = cli_runner.invoke(app, ["switch", "p"])

             assert result.exit_code == 0
             assert "Switching to personal identity" in result.output

    @patch("subprocess.run")
    def test_helper_run_git_config(self, mock_run: Mock) -> None:
        """Test run_git_config helper."""
        from menv.commands.switch import run_git_config

        # Success
        mock_run.return_value.returncode = 0
        assert run_git_config("key", "val") is True
        mock_run.assert_called_with(
            ["git", "config", "--global", "key", "val"],
            check=True,
            capture_output=True,
        )

        # Failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        assert run_git_config("key", "val") is False

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_helper_run_jj_config(self, mock_which: Mock, mock_run: Mock) -> None:
        """Test run_jj_config helper."""
        from menv.commands.switch import run_jj_config

        # jj not installed
        mock_which.return_value = None
        assert run_jj_config("key", "val") is True
        mock_run.assert_not_called()

        # Success
        mock_which.return_value = "/bin/jj"
        mock_run.return_value.returncode = 0
        assert run_jj_config("key", "val") is True
        mock_run.assert_called_with(
            ["jj", "config", "set", "--user", "key", "val"],
            check=True,
            capture_output=True,
        )

        # Failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        assert run_jj_config("key", "val") is False

    @patch("subprocess.run")
    def test_helper_get_current_git_user(self, mock_run: Mock) -> None:
        """Test get_current_git_user helper."""
        from menv.commands.switch import get_current_git_user

        # Success
        mock_run.side_effect = [
            Mock(stdout="John"),
            Mock(stdout="john@example.com"),
        ]
        assert get_current_git_user() == ("John", "john@example.com")

        # Failure
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        assert get_current_git_user() == ("", "")
