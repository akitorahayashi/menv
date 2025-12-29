"""Create command for provisioning macOS environments."""

from typing import Optional

import typer
from rich.console import Console

from menv.core.runner import run_ansible_playbook

console = Console()

VALID_PROFILES = ["macbook", "mac-mini"]


def create(
    profile: str = typer.Argument(
        ...,
        help=f"Profile to provision. Valid values: {', '.join(VALID_PROFILES)}",
    ),
    tags: Optional[str] = typer.Option(
        None,
        "--tags",
        "-t",
        help="Comma-separated list of Ansible tags to run.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output.",
    ),
) -> None:
    """Provision a macOS development environment with the specified profile.

    Examples:
        menv create macbook
        menv cr mac-mini
        menv create macbook --tags shell,python
    """
    # Validate profile
    if profile not in VALID_PROFILES:
        console.print(
            f"[bold red]Error:[/] Invalid profile '{profile}'. "
            f"Valid profiles: {', '.join(VALID_PROFILES)}"
        )
        raise typer.Exit(code=1)

    tag_list = [t.strip() for t in tags.split(",")] if tags else None

    console.print(f"[bold green]Provisioning environment:[/] {profile}")
    console.print()

    exit_code = run_ansible_playbook(
        profile=profile,
        tags=tag_list,
        verbose=verbose,
    )

    if exit_code == 0:
        console.print()
        console.print(
            "[bold green]✓ Environment provisioning completed successfully![/]"
        )
    else:
        console.print()
        console.print(f"[bold red]✗ Provisioning failed with exit code {exit_code}[/]")
        raise typer.Exit(code=exit_code)
