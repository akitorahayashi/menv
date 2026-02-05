"""Tests for ConfigDeployer service."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from menv.services.role_config_deployer import RoleConfigDeployer
from tests.mocks import MockAnsiblePaths


class TestRoleConfigDeployer:
    """Tests for the RoleConfigDeployer service."""

    @pytest.fixture
    def temp_home(self, tmp_path: Path) -> Path:
        """Create a temporary home directory."""
        home = tmp_path / "home"
        home.mkdir()
        return home

    @pytest.fixture
    def temp_ansible_dir(self, tmp_path: Path) -> Path:
        """Create a temporary ansible directory with role configs."""
        ansible_dir = tmp_path / "ansible"
        ansible_dir.mkdir()

        # Create a sample role config
        rust_config = ansible_dir / "roles" / "rust" / "config" / "common"
        rust_config.mkdir(parents=True)
        (rust_config / ".rust-version").write_text("1.75.0")
        (rust_config / "tools.yml").write_text("tools: []")

        # Create brew role with profiles
        brew_common = ansible_dir / "roles" / "brew" / "config" / "common" / "formulae"
        brew_common.mkdir(parents=True)
        (brew_common / "Brewfile").write_text("# Common Brewfile")

        brew_macbook = (
            ansible_dir / "roles" / "brew" / "config" / "profiles" / "macbook" / "cask"
        )
        brew_macbook.mkdir(parents=True)
        (brew_macbook / "Brewfile").write_text("# Macbook Brewfile")

        return ansible_dir

    @pytest.fixture
    def deployer(
        self, temp_ansible_dir: Path, temp_home: Path, monkeypatch: pytest.MonkeyPatch
    ) -> RoleConfigDeployer:
        """Create a RoleConfigDeployer with mocked paths."""
        monkeypatch.setattr(Path, "home", lambda: temp_home)
        mock_paths = MockAnsiblePaths(ansible_dir=temp_ansible_dir)
        return RoleConfigDeployer(ansible_paths=mock_paths)

    def test_list_roles_returns_roles_with_config_dirs(
        self, deployer: RoleConfigDeployer
    ) -> None:
        """Test that list_roles returns roles that have config directories."""
        roles = deployer.list_roles()

        # Should find the roles we set up in temp_ansible_dir fixture
        assert "rust" in roles
        assert "brew" in roles
        # Roles without config directories should not be included
        assert len(roles) == 2

    def test_get_local_config_path(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that local config path is correctly constructed."""
        path = deployer.get_local_config_path("rust")

        assert path == temp_home / ".config" / "menv" / "roles" / "rust"

    def test_get_package_config_path(
        self, deployer: RoleConfigDeployer, temp_ansible_dir: Path
    ) -> None:
        """Test that package config path is correctly constructed."""
        path = deployer.get_package_config_path("rust")

        assert path == temp_ansible_dir / "roles" / "rust" / "config"

    def test_is_deployed_returns_false_when_not_deployed(
        self, deployer: RoleConfigDeployer
    ) -> None:
        """Test that is_deployed returns False when config doesn't exist."""
        assert deployer.is_deployed("rust") is False

    def test_is_deployed_returns_true_after_deployment(
        self, deployer: RoleConfigDeployer
    ) -> None:
        """Test that is_deployed returns True after successful deployment."""
        deployer.create_role_config("rust")

        assert deployer.is_deployed("rust") is True

    def test_create_role_config_creates_config_directory(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_role_config creates the config directory."""
        result = deployer.create_role_config("rust")

        assert result.success is True
        assert "Created config" in result.message
        expected_path = temp_home / ".config" / "menv" / "roles" / "rust"
        assert expected_path.exists()
        assert (expected_path / "common" / ".rust-version").exists()

    def test_create_role_config_copies_files(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_role_config copies config files correctly."""
        deployer.create_role_config("rust")

        rust_version_path = (
            temp_home
            / ".config"
            / "menv"
            / "roles"
            / "rust"
            / "common"
            / ".rust-version"
        )
        assert rust_version_path.read_text() == "1.75.0"

    def test_create_role_config_skips_if_exists_without_overwrite(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_role_config skips deployment if config exists."""
        # First deployment
        deployer.create_role_config("rust")

        # Modify the local file
        local_file = (
            temp_home
            / ".config"
            / "menv"
            / "roles"
            / "rust"
            / "common"
            / ".rust-version"
        )
        local_file.write_text("1.80.0")

        # Second deployment without overwrite
        result = deployer.create_role_config("rust", overwrite=False)

        assert result.success is True
        assert "already exists" in result.message
        # File should not be overwritten
        assert local_file.read_text() == "1.80.0"

    def test_create_role_config_overwrites_with_overwrite(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_role_config overwrites config with overwrite flag."""
        # First deployment
        deployer.create_role_config("rust")

        # Modify the local file
        local_file = (
            temp_home
            / ".config"
            / "menv"
            / "roles"
            / "rust"
            / "common"
            / ".rust-version"
        )
        local_file.write_text("1.80.0")

        # Second deployment with overwrite
        result = deployer.create_role_config("rust", overwrite=True)

        assert result.success is True
        assert "Created config" in result.message
        # File should be overwritten with original value
        assert local_file.read_text() == "1.75.0"

    def test_create_role_config_fails_for_invalid_role(self, deployer: RoleConfigDeployer) -> None:
        """Test that create_role_config fails for non-existent role."""
        result = deployer.create_role_config("nonexistent")

        assert result.success is False
        assert "does not have a config directory" in result.message

    def test_create_role_config_handles_oserror(self, deployer: RoleConfigDeployer) -> None:
        """Test that create_role_config handles OSError during file operations."""
        role = "rust"

        with patch(
            "menv.services.role_config_deployer.shutil.copytree",
            side_effect=OSError("Permission denied"),
        ):
            result = deployer.create_role_config(role)

            assert result.success is False
            assert "Permission denied" in result.message

    def test_create_all_role_configs_creates_all_roles(self, deployer: RoleConfigDeployer) -> None:
        """Test that create_all_role_configs creates all roles."""
        results = deployer.create_all_role_configs()

        # All results should have success=True (either deployed or not found in package)
        successful = [r for r in results if r.success]
        assert len(successful) >= 2  # At least rust and brew should succeed

    def test_create_role_config_fails_for_role_without_config_directory(
        self, deployer: RoleConfigDeployer
    ) -> None:
        """Test that create_role_config fails for a role without a config directory."""
        # python role has no config directory in our test setup
        result = deployer.create_role_config("python")

        assert result.success is False
        assert "does not have a config directory" in result.message


class TestCreateMultipleRoleConfigs:
    """Tests for the create_multiple_role_configs method."""

    @pytest.fixture
    def temp_home(self, tmp_path: Path) -> Path:
        """Create a temporary home directory."""
        home = tmp_path / "home"
        home.mkdir()
        return home

    @pytest.fixture
    def temp_ansible_dir(self, tmp_path: Path) -> Path:
        """Create a temporary ansible directory with role configs."""
        ansible_dir = tmp_path / "ansible"
        ansible_dir.mkdir()

        # Create rust role config
        rust_config = ansible_dir / "roles" / "rust" / "config" / "common"
        rust_config.mkdir(parents=True)
        (rust_config / ".rust-version").write_text("1.75.0")

        # Create shell role config
        shell_config = ansible_dir / "roles" / "shell" / "config" / "common"
        shell_config.mkdir(parents=True)
        (shell_config / ".zshrc").write_text("# zshrc")

        # Create go role config
        go_config = ansible_dir / "roles" / "go" / "config" / "common"
        go_config.mkdir(parents=True)
        (go_config / ".go-version").write_text("1.21.0")

        return ansible_dir

    @pytest.fixture
    def deployer(
        self, temp_ansible_dir: Path, temp_home: Path, monkeypatch: pytest.MonkeyPatch
    ) -> RoleConfigDeployer:
        """Create a RoleConfigDeployer with mocked paths."""
        monkeypatch.setattr(Path, "home", lambda: temp_home)
        mock_paths = MockAnsiblePaths(ansible_dir=temp_ansible_dir)
        return RoleConfigDeployer(ansible_paths=mock_paths)

    def test_create_multiple_role_configs_creates_all_roles(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_multiple_role_configs creates all specified roles."""
        results = deployer.create_multiple_role_configs(["rust", "shell", "go"])

        assert len(results) == 3
        assert all(r.success for r in results)

        # Check all configs were deployed
        assert (temp_home / ".config" / "menv" / "roles" / "rust").exists()
        assert (temp_home / ".config" / "menv" / "roles" / "shell").exists()
        assert (temp_home / ".config" / "menv" / "roles" / "go").exists()

    def test_create_multiple_role_configs_stops_on_first_failure(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_multiple_role_configs stops on first failure."""
        # Include an invalid role in the middle
        results = deployer.create_multiple_role_configs(["rust", "nonexistent", "shell"])

        # Should have 2 results: rust (success) and nonexistent (failure)
        assert len(results) == 2
        assert results[0].success is True
        assert results[0].role == "rust"
        assert results[1].success is False
        assert results[1].role == "nonexistent"

        # shell should NOT be deployed because we stopped early
        assert not (temp_home / ".config" / "menv" / "roles" / "shell").exists()

    def test_create_multiple_role_configs_empty_list(self, deployer: RoleConfigDeployer) -> None:
        """Test that create_multiple_role_configs with empty list returns empty results."""
        results = deployer.create_multiple_role_configs([])

        assert results == []

    def test_create_multiple_role_configs_with_overwrite(
        self, deployer: RoleConfigDeployer, temp_home: Path
    ) -> None:
        """Test that create_multiple_role_configs respects overwrite flag."""
        # First deployment
        deployer.create_multiple_role_configs(["rust"])

        # Modify local file
        local_file = (
            temp_home
            / ".config"
            / "menv"
            / "roles"
            / "rust"
            / "common"
            / ".rust-version"
        )
        local_file.write_text("modified")

        # Second deployment with overwrite
        results = deployer.create_multiple_role_configs(["rust"], overwrite=True)

        assert len(results) == 1
        assert results[0].success is True
        # File should be overwritten
        assert local_file.read_text() == "1.75.0"
