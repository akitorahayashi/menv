"""Tests for create command."""

from __future__ import annotations

from unittest.mock import Mock

from typer.testing import CliRunner

from menv.context import AppContext
from menv.main import app


class TestCreateCommand:
    """Tests for the create command."""

    def test_create_help_shows_profile_argument(self, cli_runner: CliRunner) -> None:
        """Test that create --help shows profile argument."""
        result = cli_runner.invoke(app, ["create", "--help"])

        assert result.exit_code == 0
        assert "PROFILE" in result.output or "profile" in result.output.lower()

    def test_cr_alias_works(self, cli_runner: CliRunner) -> None:
        """Test that 'cr' alias for create works."""
        result = cli_runner.invoke(app, ["cr", "--help"])

        assert result.exit_code == 0
        assert "PROFILE" in result.output or "profile" in result.output.lower()

    def test_create_invalid_profile_shows_error(self, cli_runner: CliRunner) -> None:
        """Test that invalid profile for create shows error."""
        result = cli_runner.invoke(app, ["create", "invalid-profile"])

        assert result.exit_code != 0
        assert "Invalid profile" in result.output or "Error" in result.output

    def test_create_requires_profile_argument(self, cli_runner: CliRunner) -> None:
        """Test that create without profile shows error."""
        result = cli_runner.invoke(app, ["create"])

        # Should show error about missing argument
        assert result.exit_code != 0 or "PROFILE" in result.output

    def test_create_runs_full_setup(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test that create runs full setup with expected calls."""
        mock_runner = mock_app_context.ansible_runner

        result = cli_runner.invoke(app, ["create", "macbook"])

        assert result.exit_code == 0
        assert "Creating macbook environment" in result.output
        assert "Deploying configurations" in result.output
        assert "Environment created successfully" in result.output

        # Verify runner calls
        # We expect multiple calls to run_playbook, one for each tag in FULL_SETUP_TAGS
        assert len(mock_runner.calls) > 0

        # Verify first call is brew-formulae
        assert mock_runner.calls[0]["tags"] == ["brew-formulae"]
        assert mock_runner.calls[0]["profile"] == "macbook"

    def test_create_with_overwrite(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test create with overwrite flag."""
        # Setup config deployer to return success
        mock_deployer = mock_app_context.config_deployer

        # Patch deploy_multiple_roles to verify call
        mock_deployer.deploy_multiple_roles = Mock(wraps=mock_deployer.deploy_multiple_roles)

        result = cli_runner.invoke(app, ["create", "mac-mini", "--overwrite"])

        assert result.exit_code == 0

        # Verify deployer was called with overwrite=True
        mock_deployer.deploy_multiple_roles.assert_called()
        args, kwargs = mock_deployer.deploy_multiple_roles.call_args
        assert kwargs["overwrite"] is True

    def test_create_fails_if_runner_fails(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test that create stops if a step fails."""
        mock_runner = mock_app_context.ansible_runner

        # Make the runner fail on the first call
        mock_runner.exit_code = 1

        result = cli_runner.invoke(app, ["create", "macbook"])

        assert result.exit_code == 1
        assert "Failed with exit code 1" in result.output
        assert "Setup failed at step" in result.output

    def test_create_handles_aliases(
        self, cli_runner: CliRunner, mock_app_context: AppContext
    ) -> None:
        """Test that aliases are resolved (mbk -> macbook)."""
        mock_runner = mock_app_context.ansible_runner

        result = cli_runner.invoke(app, ["create", "mbk"])

        assert result.exit_code == 0
        assert "Creating macbook environment" in result.output

        # Verify profile passed to runner is resolved
        assert mock_runner.calls[0]["profile"] == "macbook"
