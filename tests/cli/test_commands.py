"""Integration tests for CLI commands."""

from __future__ import annotations

from typer.testing import CliRunner

from menv.main import app


class TestCLIIntegration:
    """Integration tests for CLI command interactions."""

    def test_version_flag_shows_version(self, cli_runner: CliRunner) -> None:
        """Test that --version flag shows version information."""
        result = cli_runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "menv version:" in result.output

    def test_short_version_flag_shows_version(self, cli_runner: CliRunner) -> None:
        """Test that -V flag shows version information."""
        result = cli_runner.invoke(app, ["-V"])

        assert result.exit_code == 0
        assert "menv version:" in result.output

    def test_help_flag_shows_help(self, cli_runner: CliRunner) -> None:
        """Test that --help flag shows help information."""
        result = cli_runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "menv" in result.output
        assert "create" in result.output
        assert "update" in result.output

    def test_no_args_shows_help(self, cli_runner: CliRunner) -> None:
        """Test that running without arguments shows help."""
        result = cli_runner.invoke(app, [])

        assert "Usage:" in result.output or "menv" in result.output

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

    def test_update_help_shows_description(self, cli_runner: CliRunner) -> None:
        """Test that update --help shows description."""
        result = cli_runner.invoke(app, ["update", "--help"])

        assert result.exit_code == 0
        # Should mention update or version
        assert "update" in result.output.lower() or "version" in result.output.lower()

    def test_u_alias_works(self, cli_runner: CliRunner) -> None:
        """Test that 'u' alias for update works."""
        result = cli_runner.invoke(app, ["u", "--help"])

        assert result.exit_code == 0

    def test_create_invalid_profile_shows_error(self, cli_runner: CliRunner) -> None:
        """Test that invalid profile shows error."""
        result = cli_runner.invoke(app, ["create", "invalid-profile"])

        assert result.exit_code != 0
        assert "Invalid profile" in result.output or "Error" in result.output

    def test_create_requires_profile_argument(self, cli_runner: CliRunner) -> None:
        """Test that create without profile shows help."""
        result = cli_runner.invoke(app, ["create"])

        # Should either show help or error about missing argument
        assert result.exit_code != 0 or "PROFILE" in result.output
