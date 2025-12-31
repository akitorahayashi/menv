"""Tests for phases module."""

from __future__ import annotations

from menv.models.phases import Phase, get_optional_commands, get_phases


class TestPhase:
    """Tests for Phase dataclass."""

    def test_phase_has_required_fields(self) -> None:
        """Test that Phase has all required fields."""
        phase = Phase(
            name="Test",
            description="Test description",
            commands=["cmd1", "cmd2"],
        )

        assert phase.name == "Test"
        assert phase.description == "Test description"
        assert phase.commands == ["cmd1", "cmd2"]
        assert phase.parallel is True
        assert phase.dependencies == []

    def test_phase_with_dependencies(self) -> None:
        """Test that Phase can have dependencies."""
        phase = Phase(
            name="Tools",
            description="Install tools",
            commands=["menv make python-tools"],
            dependencies=["Language Runtimes"],
        )

        assert phase.dependencies == ["Language Runtimes"]


class TestGetPhases:
    """Tests for get_phases function."""

    def test_returns_phases_for_macbook(self) -> None:
        """Test that phases are returned for macbook profile."""
        phases = get_phases("macbook")

        assert len(phases) == 4
        assert phases[0].name == "Configuration"
        assert phases[1].name == "Language Runtimes"
        assert phases[2].name == "Tools"
        assert phases[3].name == "Editors"

    def test_returns_phases_for_mac_mini(self) -> None:
        """Test that phases are returned for mac-mini profile."""
        phases = get_phases("mac-mini")

        assert len(phases) == 4
        # All commands should include mac-mini profile
        for phase in phases:
            for cmd in phase.commands:
                assert "mac-mini" in cmd

    def test_configuration_phase_has_parallel_commands(self) -> None:
        """Test that configuration phase has parallel-runnable commands."""
        phases = get_phases("macbook")
        config_phase = phases[0]

        assert config_phase.parallel is True
        assert "shell" in config_phase.commands[0]
        assert "system" in config_phase.commands[1]

    def test_tools_phase_has_dependencies(self) -> None:
        """Test that tools phase depends on language runtimes."""
        phases = get_phases("macbook")
        tools_phase = phases[2]

        assert "Language Runtimes" in tools_phase.dependencies

    def test_all_commands_include_profile(self) -> None:
        """Test that all commands include the profile."""
        phases = get_phases("macbook")

        for phase in phases:
            for cmd in phase.commands:
                # Extract the base command (before any comments)
                base_cmd = cmd.split("#")[0].strip()
                assert "macbook" in base_cmd


class TestGetOptionalCommands:
    """Tests for get_optional_commands function."""

    def test_returns_optional_commands(self) -> None:
        """Test that optional commands are returned."""
        commands = get_optional_commands("macbook")

        assert len(commands) > 0
        assert any("brew-formulae" in cmd for cmd in commands)
        assert any("ssh" in cmd for cmd in commands)

    def test_commands_include_profile(self) -> None:
        """Test that optional commands include the profile."""
        commands = get_optional_commands("mac-mini")

        for cmd in commands:
            base_cmd = cmd.split("#")[0].strip()
            assert "mac-mini" in base_cmd
