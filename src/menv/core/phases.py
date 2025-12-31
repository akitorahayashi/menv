"""Phase definitions for setup guide."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Phase:
    """A setup phase with commands to run."""

    name: str
    description: str
    commands: list[str]
    parallel: bool = True
    dependencies: list[str] = field(default_factory=list)


def get_phases(profile: str) -> list[Phase]:
    """Get all phases for the given profile.

    Args:
        profile: The profile name (macbook, mac-mini).

    Returns:
        List of Phase objects defining the setup stages.
    """
    return [
        Phase(
            name="Configuration",
            description="These can run in parallel - open multiple terminals if you want:",
            commands=[
                f"menv make shell {profile}",
                f"menv make system {profile}",
                f"menv make git {profile}",
                f"menv make jj {profile}",
                f"menv make gh {profile}",
            ],
            parallel=True,
        ),
        Phase(
            name="Language Runtimes",
            description="These can run in parallel:",
            commands=[
                f"menv make python-platform {profile}",
                f"menv make nodejs-platform {profile}",
                f"menv make ruby {profile}",
                f"menv make rust-platform {profile}",
                f"menv make go-platform {profile}",
            ],
            parallel=True,
        ),
        Phase(
            name="Tools",
            description="Run after the corresponding runtime is installed:",
            commands=[
                f"menv make python-tools {profile}  # requires: python-platform",
                f"menv make uv {profile}            # requires: python-tools",
                f"menv make nodejs-tools {profile}  # requires: nodejs-platform",
                f"menv make rust-tools {profile}    # requires: rust-platform",
                f"menv make go-tools {profile}      # requires: go-platform",
            ],
            parallel=True,
            dependencies=["Language Runtimes"],
        ),
        Phase(
            name="Editors",
            description="Configuration and extensions (apps should be pre-installed):",
            commands=[
                f"menv make vscode {profile}",
                f"menv make cursor {profile}",
                f"menv make coderabbit {profile}",
            ],
            parallel=True,
        ),
    ]


def get_optional_commands(profile: str) -> list[str]:
    """Get optional commands that can be run after main setup.

    Args:
        profile: The profile name.

    Returns:
        List of optional command strings.
    """
    return [
        f"menv make brew-formulae {profile}  # Additional CLI tools",
        f"menv make brew-cask {profile}      # GUI applications",
        f"menv make ssh {profile}            # SSH configuration",
        f"menv make aider {profile}          # Aider AI assistant",
        f"menv make llm {profile}            # LLM tools",
    ]
