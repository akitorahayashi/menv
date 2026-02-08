"""Tests for system backup service."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from menv.services.backup.system import SystemBackupService, BackupError


class TestSystemBackupService:
    @patch("menv.services.backup.system.subprocess.run")
    def test_backup_success(self, mock_run, tmp_path):
        service = SystemBackupService()
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        definitions_dir = config_dir / "definitions"
        definitions_dir.mkdir()

        # Create a dummy definition
        yaml_content = "- { key: 'testKey', type: 'string', default: 'default' }"
        (definitions_dir / "test.yml").write_text(yaml_content)

        mock_run.return_value.stdout = "value"
        mock_run.return_value.returncode = 0

        output = tmp_path / "output.yml"

        assert service.backup(config_dir, output=output) == 0

        assert output.exists()
        content = output.read_text()
        assert 'key: "testKey"' in content
        assert 'value: "value"' in content

    @patch("menv.services.backup.system.subprocess.run")
    def test_backup_defaults_command_missing(self, mock_run, tmp_path):
        service = SystemBackupService()
        config_dir = tmp_path / "config"
        definitions_dir = config_dir / "definitions"
        definitions_dir.mkdir(parents=True)
        yaml_content = "- { key: 'testKey', type: 'string', default: 'default' }"
        (definitions_dir / "test.yml").write_text(yaml_content)

        mock_run.side_effect = FileNotFoundError

        # backup catches BackupError and prints to stderr, returns 1
        assert service.backup(config_dir, definitions_dir=definitions_dir) == 1

    @patch("menv.services.backup.system.subprocess.run")
    def test_backup_defaults_command_failed(self, mock_run, tmp_path):
        service = SystemBackupService()
        config_dir = tmp_path / "config"
        definitions_dir = config_dir / "definitions"
        definitions_dir.mkdir(parents=True)
        yaml_content = "- { key: 'testKey', type: 'string', default: 'default' }"
        (definitions_dir / "test.yml").write_text(yaml_content)

        # subprocess.run raises CalledProcessError if check=True and return code is not 0
        mock_run.side_effect = subprocess.CalledProcessError(1, ["defaults"])

        output = tmp_path / "output.yml"
        assert service.backup(config_dir, definitions_dir=definitions_dir, output=output) == 0

        # Should use default value
        content = output.read_text()
        assert 'value: "default"' in content

    def test_iter_definitions_invalid_yaml(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "invalid.yml").write_text(": invalid")

        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    def test_iter_definitions_missing_key(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "missing_key.yml").write_text("- { type: 'string' }")

        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    @patch("menv.services.backup.system.subprocess.run")
    def test_format_types(self, mock_run, tmp_path):
        service = SystemBackupService()
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        definitions_dir = config_dir / "definitions"
        definitions_dir.mkdir(parents=True)

        yaml_content = """
- { key: 'boolTrue', type: 'bool', default: true }
- { key: 'boolFalse', type: 'bool', default: false }
- { key: 'intVal', type: 'int', default: 10 }
- { key: 'floatVal', type: 'float', default: 10.5 }
- { key: 'specialKey', type: 'string', default: 'val' }
        """
        (definitions_dir / "types.yml").write_text(yaml_content)

        # Mock responses
        def side_effect(command, **kwargs):
            key = command[-1]
            if key == "boolTrue":
                return MagicMock(stdout="1\n", returncode=0)
            if key == "boolFalse":
                return MagicMock(stdout="0\n", returncode=0)
            if key == "intVal":
                return MagicMock(stdout="20\n", returncode=0)
            if key == "floatVal":
                return MagicMock(stdout="20.5\n", returncode=0)
            if key == "specialKey":
                 if "-g" in command:
                     return MagicMock(stdout="special\n", returncode=0)
            return MagicMock(stdout="\n", returncode=1)

        mock_run.side_effect = side_effect

        output = tmp_path / "output.yml"

        # Update SPECIAL_GLOBAL_KEYS to include 'specialKey' for testing
        with patch("menv.services.backup.system.SPECIAL_GLOBAL_KEYS", {"specialKey"}):
             service.backup(config_dir, definitions_dir=definitions_dir, output=output)

        content = output.read_text()
        assert 'value: true' in content
        assert 'value: false' in content
        assert 'value: 20' in content
        assert 'value: 20.5' in content
        assert 'value: "special"' in content

    def test_backup_missing_definitions_dir(self, tmp_path):
        service = SystemBackupService()
        config_dir = tmp_path / "config"
        # don't create definitions dir
        assert service.backup(config_dir) == 1

    def test_iter_definitions_not_dict(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "not_dict.yml").write_text("- string_entry")
        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    def test_iter_definitions_invalid_domain(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "invalid_domain.yml").write_text("- { key: 'k', domain: 123 }")
        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    def test_iter_definitions_missing_type(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "missing_type.yml").write_text("- { key: 'k', domain: 'd' }")
        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    def test_iter_definitions_invalid_comment(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "invalid_comment.yml").write_text("- { key: 'k', type: 'string', comment: 123 }")
        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    def test_load_yaml_empty(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "empty.yml").write_text("")
        output = tmp_path / "output.yml"

        assert service.backup(tmp_path, definitions_dir=definitions_dir, output=output) == 0
        assert output.read_text().strip() == "---"

    def test_load_yaml_not_list(self, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "dict.yml").write_text("key: value")
        assert service.backup(tmp_path, definitions_dir=definitions_dir) == 1

    @patch("menv.services.backup.system.subprocess.run")
    def test_format_numeric_error(self, mock_run, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "num.yml").write_text("- { key: 'k', type: 'int', default: 0 }")

        mock_run.return_value.stdout = "not_a_number"
        mock_run.return_value.returncode = 0

        output = tmp_path / "output.yml"
        assert service.backup(tmp_path, definitions_dir=definitions_dir, output=output) == 0
        assert 'value: not_a_number' in output.read_text()

    @patch("menv.services.backup.system.subprocess.run")
    def test_format_string_home(self, mock_run, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "str.yml").write_text("- { key: 'location', type: 'string' }")

        home = str(Path.home())
        mock_run.return_value.stdout = f"{home}/some/path"
        mock_run.return_value.returncode = 0

        output = tmp_path / "output.yml"
        assert service.backup(tmp_path, definitions_dir=definitions_dir, output=output) == 0
        assert 'value: "$HOME/some/path"' in output.read_text()

    @patch("menv.services.backup.system.subprocess.run")
    def test_format_bool_defaults(self, mock_run, tmp_path):
        service = SystemBackupService()
        definitions_dir = tmp_path / "definitions"
        definitions_dir.mkdir()
        (definitions_dir / "bool.yml").write_text("""
- { key: 'b1', type: 'bool', default: 'true' }
- { key: 'b2', type: 'bool', default: true }
- { key: 'b3', type: 'bool' }
        """)

        mock_run.side_effect = subprocess.CalledProcessError(1, ["defaults"])

        output = tmp_path / "output.yml"
        assert service.backup(tmp_path, definitions_dir=definitions_dir, output=output) == 0
        content = output.read_text()
        assert 'value: true' in content
