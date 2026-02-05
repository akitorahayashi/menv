"""Protocol definitions for menv."""

from menv.protocols.ansible_paths import AnsiblePathsProtocol
from menv.protocols.ansible_runner import AnsibleRunnerProtocol
from menv.protocols.identity_storage import IdentityStorageProtocol
from menv.protocols.playbook import PlaybookProtocol
from menv.protocols.role_config_deployer import (
    RoleConfigCreateResult,
    RoleConfigDeployerProtocol,
)
from menv.protocols.version_checker import VersionCheckerProtocol

__all__ = [
    "AnsiblePathsProtocol",
    "AnsibleRunnerProtocol",
    "RoleConfigDeployerProtocol",
    "IdentityStorageProtocol",
    "RoleConfigCreateResult",
    "PlaybookProtocol",
    "VersionCheckerProtocol",
]
