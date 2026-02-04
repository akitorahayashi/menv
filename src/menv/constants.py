"""Global constants for menv."""

from pathlib import Path

CONFIG_DIR_NAME = "menv"
CONFIG_ROOT = Path.home() / ".config" / CONFIG_DIR_NAME
ROLES_DIR = CONFIG_ROOT / "roles"
