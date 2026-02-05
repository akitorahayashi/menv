"""Tests for AnsibleRunner service."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import cast
from unittest.mock import MagicMock, Mock, patch

import pytest
from rich.console import Console

from menv.protocols.ansible_paths import AnsiblePathsProtocol
from menv.services.ansible_runner import AnsibleRunner


class TestAnsibleRunner:
    """Tests for AnsibleRunner."""

    @pytest.fixture
    def mock_paths(self) -> AnsiblePathsProtocol:
        """Mock AnsiblePaths."""
        paths = Mock(spec=AnsiblePathsProtocol)
        # Mock paths
        ansible_dir = Path("/mock/ansible")
        paths.ansible_dir.return_value = ansible_dir
        return paths

    @pytest.fixture
    def mock_console(self) -> Console:
        """Mock Console."""
        return Mock(spec=Console)

    @pytest.fixture
    def runner(
        self, mock_paths: AnsiblePathsProtocol, mock_console: Console
    ) -> AnsibleRunner:
        """Create AnsibleRunner instance."""
        return AnsibleRunner(paths=mock_paths, console=mock_console)

    @patch("subprocess.Popen")
    def test_run_playbook_success(
        self,
        mock_popen: MagicMock,
        runner: AnsibleRunner,
        mock_paths: AnsiblePathsProtocol,
        mock_console: Console,
    ) -> None:
        """Test successful playbook execution."""
        # Setup mock process
        process = Mock()
        process.returncode = 0
        process.stdout = ["line1\n", "line2\n"]
        process.wait.return_value = None
        mock_popen.return_value = process

        # Run
        exit_code = runner.run_playbook("macbook", tags=["tag1", "tag2"], verbose=True)

        # Verify
        assert exit_code == 0

        # Verify command construction
        mock_popen.assert_called_once()
        args, kwargs = mock_popen.call_args
        cmd = args[0]

        assert cmd[0] == "ansible-playbook"
        assert str(mock_paths.ansible_dir() / "playbook.yml") in cmd
        assert "-e" in cmd
        assert "profile=macbook" in cmd
        assert "--tags" in cmd
        assert "tag1,tag2" in cmd
        assert "-vvv" in cmd  # verbose=True

        # Verify environment
        env = kwargs["env"]
        assert env["ANSIBLE_CONFIG"] == str(mock_paths.ansible_dir() / "ansible.cfg")

        # Verify console output
        cast(Mock, mock_console.print).assert_called()

    @patch("subprocess.Popen")
    def test_run_playbook_streaming_output(
        self,
        mock_popen: MagicMock,
        runner: AnsibleRunner,
    ) -> None:
        """Test that stdout is streamed."""
        # Setup mock process
        process = Mock()
        process.returncode = 0
        process.stdout = ["output line 1\n", "output line 2\n"]
        mock_popen.return_value = process

        # Capture sys.stdout
        with patch("sys.stdout") as mock_stdout:
            runner.run_playbook("macbook")

            # Verify writes
            mock_stdout.write.assert_any_call("output line 1\n")
            mock_stdout.write.assert_any_call("output line 2\n")
            mock_stdout.flush.assert_called()

    @patch("subprocess.Popen")
    def test_run_playbook_file_not_found(
        self,
        mock_popen: MagicMock,
        runner: AnsibleRunner,
        mock_console: Console,
    ) -> None:
        """Test handling of FileNotFoundError (ansible not installed)."""
        mock_popen.side_effect = FileNotFoundError

        exit_code = runner.run_playbook("macbook")

        assert exit_code == 1
        cast(Mock, mock_console.print).assert_called_with(
            "[bold red]Error:[/] ansible-playbook not found. Please ensure Ansible is installed."
        )

    @patch("subprocess.Popen")
    def test_run_playbook_keyboard_interrupt(
        self,
        mock_popen: MagicMock,
        runner: AnsibleRunner,
        mock_console: Console,
    ) -> None:
        """Test handling of KeyboardInterrupt."""
        mock_popen.side_effect = KeyboardInterrupt

        exit_code = runner.run_playbook("macbook")

        assert exit_code == 130
        cast(Mock, mock_console.print).assert_called_with("\n[yellow]Interrupted by user[/]")

    @patch("subprocess.Popen")
    def test_run_playbook_failure(
        self,
        mock_popen: MagicMock,
        runner: AnsibleRunner,
    ) -> None:
        """Test execution failure (non-zero exit code)."""
        process = Mock()
        process.returncode = 2
        process.stdout = []
        mock_popen.return_value = process

        exit_code = runner.run_playbook("macbook")

        assert exit_code == 2
