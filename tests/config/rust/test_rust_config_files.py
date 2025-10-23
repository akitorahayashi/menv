from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml


def _load_yaml(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:  # pragma: no cover - exercised via pytest.fail
        pytest.fail(f"Invalid YAML syntax in {path.name}: {exc}")


class TestRustConfigs:
    def test_rust_components_schema(self, rust_config_dir: Path) -> None:
        config_path = rust_config_dir / "rust-components.yml"
        data = _load_yaml(config_path)

        assert isinstance(
            data, dict
        ), "rust-components.yml must define a mapping at the top level."
        assert (
            "components" in data
        ), "'components' key missing from rust-components.yml."

        components = data["components"]
        assert isinstance(components, list), "'components' must be a list."

        for index, component in enumerate(components):
            assert isinstance(
                component, str
            ), f"Component #{index + 1} must be a string."
            assert component.strip(), f"Component #{index + 1} must not be empty."

    def test_tools_schema(self, rust_config_dir: Path) -> None:
        config_path = rust_config_dir / "tools.yml"
        data = _load_yaml(config_path)

        assert isinstance(
            data, dict
        ), "tools.yml must define a mapping at the top level."
        assert "tools" in data, "'tools' key missing from tools.yml."

        tools = data["tools"]
        assert isinstance(tools, list), "'tools' must be a list."

        if not tools:
            pytest.skip("No tools defined; skipping detailed schema validation.")

        for index, tool in enumerate(tools, start=1):
            assert isinstance(tool, dict), f"Tool #{index} must be a mapping."
            assert "name" in tool, f"Tool #{index} is missing the required 'name' key."
            assert (
                isinstance(tool["name"], str) and tool["name"].strip()
            ), f"Tool #{index} 'name' must be a non-empty string."

            for optional_key in ("git", "tag", "options"):
                if optional_key in tool:
                    assert isinstance(
                        tool[optional_key], str
                    ), f"Tool #{index} optional key '{optional_key}' must be a string."
                    assert tool[
                        optional_key
                    ].strip(), f"Tool #{index} optional key '{optional_key}' must not be empty."
