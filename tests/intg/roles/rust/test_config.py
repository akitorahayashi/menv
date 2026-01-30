from __future__ import annotations

from pathlib import Path

import pytest
import yaml


class TestRustConfigs:
    def test_rust_components_schema(self, rust_config_dir: Path) -> None:
        components_file = rust_config_dir / "rust-components.yml"
        data = yaml.safe_load(components_file.read_text())

        assert isinstance(data, dict), "rust-components.yml must define a mapping."
        assert "components" in data, "Missing 'components' key in rust-components.yml."
        assert set(data.keys()) == {"components"}, (
            "rust-components.yml must have exactly one key: 'components'. "
            f"Found: {', '.join(sorted(data.keys())) or 'none'}"
        )

        components = data["components"]
        assert isinstance(components, list), "'components' must be a list."
        for index, component in enumerate(components):
            assert isinstance(component, str), (
                f"Component #{index + 1} in rust-components.yml must be a string."
            )
            assert component.strip(), (
                f"Component #{index + 1} in rust-components.yml cannot be empty."
            )

    def test_tools_schema(self, rust_config_dir: Path) -> None:
        """Validate tools.yml schema for GitHub release binary downloads."""
        tools_file = rust_config_dir / "tools.yml"
        data = yaml.safe_load(tools_file.read_text())

        assert isinstance(data, dict), "tools.yml must define a mapping."
        assert "tools" in data, "Missing 'tools' key in tools.yml."
        assert set(data.keys()) == {"tools"}, (
            "tools.yml must have exactly one key: 'tools'. "
            f"Found: {', '.join(sorted(data.keys())) or 'none'}"
        )

        tools = data["tools"]
        assert isinstance(tools, list), "'tools' must be a list."

        required_keys = {"name", "repo", "tag"}
        for index, tool in enumerate(tools):
            assert isinstance(tool, dict), f"Tool #{index + 1} must be a mapping."

            for key in required_keys:
                assert key in tool, f"Tool #{index + 1} is missing required key '{key}'."
                assert isinstance(tool[key], str), (
                    f"Tool #{index + 1} has a non-string '{key}' value."
                )
                assert tool[key].strip(), (
                    f"Tool #{index + 1} cannot have an empty '{key}'."
                )

            extra_keys = set(tool.keys()) - required_keys
            assert not extra_keys, (
                f"Tool #{index + 1} has unexpected keys: {', '.join(sorted(extra_keys))}"
            )

        if not tools:
            pytest.skip("No tools defined in tools.yml to validate further.")

    def test_tools_repo_format(self, rust_config_dir: Path) -> None:
        """Validate repo field follows owner/name format."""
        tools_file = rust_config_dir / "tools.yml"
        data = yaml.safe_load(tools_file.read_text())
        tools = data["tools"]

        for index, tool in enumerate(tools):
            repo = tool["repo"]
            parts = repo.split("/")
            assert len(parts) == 2, (
                f"Tool #{index + 1} ({tool['name']}) has invalid repo format: {repo}. "
                "Expected 'owner/name'."
            )

    def test_platforms_schema(self, rust_config_dir: Path) -> None:
        """Validate platforms.yml schema for OS and architecture mapping."""
        platforms_file = rust_config_dir / "platforms.yml"
        data = yaml.safe_load(platforms_file.read_text())

        assert isinstance(data, dict), "platforms.yml must define a mapping."
        assert "os_mapping" in data, "Missing 'os_mapping' in platforms.yml."
        assert "arch_mapping" in data, "Missing 'arch_mapping' in platforms.yml."

        os_mapping = data["os_mapping"]
        assert isinstance(os_mapping, dict), "'os_mapping' must be a mapping."
        assert "Darwin" in os_mapping, "Missing Darwin in os_mapping."
        assert "Linux" in os_mapping, "Missing Linux in os_mapping."

        arch_mapping = data["arch_mapping"]
        assert isinstance(arch_mapping, dict), "'arch_mapping' must be a mapping."
        assert "x86_64" in arch_mapping, "Missing x86_64 in arch_mapping."
        assert "aarch64" in arch_mapping, "Missing aarch64 in arch_mapping."
