import json
from pathlib import Path

import pytest
import yaml


@pytest.fixture(scope="session")
def editor_tasks_dir(project_root: Path) -> Path:
    """Editor role tasks directory."""
    return project_root / "src/menv/ansible/roles/editor/tasks"


class TestAntigravityTask:
    def test_antigravity_task_file_exists(self, editor_tasks_dir: Path) -> None:
        """Verify antigravity.yml task file exists."""
        antigravity_task = editor_tasks_dir / "antigravity.yml"
        assert antigravity_task.exists(), "antigravity.yml task file not found"

    def test_antigravity_task_valid_yaml(self, editor_tasks_dir: Path) -> None:
        """Verify antigravity.yml has valid YAML syntax."""
        antigravity_task = editor_tasks_dir / "antigravity.yml"
        with antigravity_task.open("r") as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML in antigravity.yml: {e}")


class TestAntigravityExtensions:
    def test_extensions_file_exists(self, editor_config_base: Path) -> None:
        """Verify antigravity-extensions.json exists."""
        extensions_file = editor_config_base / "antigravity-extensions.json"
        assert extensions_file.exists(), "antigravity-extensions.json not found"

    def test_extensions_non_empty(self, editor_config_base: Path) -> None:
        """Verify antigravity extensions list is non-empty."""
        extensions_file = editor_config_base / "antigravity-extensions.json"
        with extensions_file.open("r") as f:
            data = json.load(f)

        assert "extensions" in data, "Missing 'extensions' key"
        extensions = data["extensions"]
        assert isinstance(extensions, list), "extensions must be a list"
        assert len(extensions) > 0, "extensions list should not be empty"
