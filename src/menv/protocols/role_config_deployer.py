"""Protocol for role config deployment operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class RoleConfigCreateResult:
    """Result of a role config creation operation."""

    role: str
    success: bool
    message: str
    path: Path | None = None


class RoleConfigDeployerProtocol(Protocol):
    """Role config deployment abstraction."""

    @property
    def roles_with_config(self) -> list[str]:
        """Get list of roles that have config directories.

        Returns:
            Sorted list of role names that have config directories.
        """
        ...

    def create_role_config(self, role: str, overwrite: bool = False) -> RoleConfigCreateResult:
        """Create config for a single role in ~/.config/menv/roles/{role}/.

        Args:
            role: The role name to create config for.
            overwrite: If True, overwrite existing config.

        Returns:
            RoleConfigCreateResult with success status and message.
        """
        ...

    def create_all_role_configs(self, overwrite: bool = False) -> list[RoleConfigCreateResult]:
        """Create configs for all roles.

        Args:
            overwrite: If True, overwrite existing configs.

        Returns:
            List of RoleConfigCreateResult for each role.
        """
        ...

    def get_local_config_path(self, role: str) -> Path:
        """Get the local config path for a role.

        Args:
            role: The role name.

        Returns:
            Path to ~/.config/menv/roles/{role}/.
        """
        ...

    def get_package_config_path(self, role: str) -> Path:
        """Get the package config path for a role.

        Args:
            role: The role name.

        Returns:
            Path to package ansible/roles/{role}/config/.
        """
        ...

    def is_deployed(self, role: str) -> bool:
        """Check if a role's config is already deployed.

        Args:
            role: The role name.

        Returns:
            True if config exists at local path.
        """
        ...

    def list_roles(self) -> list[str]:
        """List all available roles with configs.

        Returns:
            List of role names that have config directories.
        """
        ...

    def create_multiple_role_configs(
        self, roles: list[str], overwrite: bool = False
    ) -> list[RoleConfigCreateResult]:
        """Create configs for multiple roles, stopping on first failure.

        Args:
            roles: List of role names to create configs for.
            overwrite: If True, overwrite existing configs.

        Returns:
            List of RoleConfigCreateResult for each role attempted.
            Stops early if any creation fails.
        """
        ...
