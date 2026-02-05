"""Type definitions for menv configuration."""

from __future__ import annotations

from typing import Any, TypedDict


class IdentityConfigValidationError(Exception):
    """Configuration validation error."""


class VcsIdentityConfig(TypedDict):
    """Identity configuration for VCS."""

    name: str
    email: str


class IdentityConfig(TypedDict):
    """Full menv configuration."""

    personal: VcsIdentityConfig
    work: VcsIdentityConfig


def validate_config(data: Any) -> IdentityConfig:
    """Validate configuration data.

    Args:
        data: Raw configuration data.

    Returns:
        Validated configuration.

    Raises:
        IdentityConfigValidationError: If configuration is invalid.
    """
    if not isinstance(data, dict):
        raise IdentityConfigValidationError("Configuration must be a dictionary.")

    for section in ["personal", "work"]:
        if section not in data:
            raise IdentityConfigValidationError(f"Missing section: '{section}'")

        section_data = data[section]
        if not isinstance(section_data, dict):
            raise IdentityConfigValidationError(f"Section '{section}' must be a dictionary.")

        for field in ["name", "email"]:
            if field not in section_data:
                raise IdentityConfigValidationError(f"Missing field in '{section}': '{field}'")

            value = section_data[field]
            if not isinstance(value, str):
                raise IdentityConfigValidationError(
                    f"Field '{section}.{field}' must be a string."
                )

            if not value.strip():
                raise IdentityConfigValidationError(
                    f"Field '{section}.{field}' cannot be empty."
                )

    return data  # type: ignore
