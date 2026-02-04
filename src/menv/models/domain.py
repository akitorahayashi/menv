"""Domain model definitions for menv."""

from __future__ import annotations

# Predefined tag groups that combine multiple tags
TAG_GROUPS = {
    "rust": ["rust-platform", "rust-tools"],
    "python": ["python-platform", "python-tools"],
    "nodejs": ["nodejs-platform", "nodejs-tools"],
    "go": ["go-platform", "go-tools"],
}

# Valid profiles and their aliases
VALID_PROFILES = {"common", "macbook", "mac-mini"}

PROFILE_ALIASES = {
    "mmn": "mac-mini",
    "mbk": "macbook",
    "cmn": "common",
}

# Ordered list of tags for full setup
# This defines the execution order for a complete environment setup
FULL_SETUP_TAGS = [
    # Phase 0: Brew dependencies (must be first)
    "brew-formulae",
    "ollama",
    # Phase 1: Configuration
    "shell",
    "system",
    "git",
    "jj",
    "gh",
    # Phase 2: Language runtimes
    "python-platform",
    "nodejs-platform",
    "ruby",
    "rust-platform",
    "go-platform",
    # Phase 3: Language tools (require runtimes)
    "python-tools",
    "uv",
    "nodejs-tools",
    "rust-tools",
    "go-tools",
    # Phase 4: Editors
    "vscode",
    "cursor",
    # Phase 5: Additional tools
    "aider",
    "coder",
    "mlx",
    "xcode",
]
