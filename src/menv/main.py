"""Typer CLI application entry point for menv."""

from importlib import metadata
from typing import Optional

import typer
from rich.console import Console

from menv.commands.create import create
from menv.commands.update import update

console = Console()


def get_safe_version(package_name: str, fallback: str = "0.1.0") -> str:
    """Safely get the version of a package.

    Args:
        package_name: Name of the package.
        fallback: Default version if retrieval fails.

    Returns:
        Version string.
    """
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return fallback


def version_callback(value: Optional[bool]) -> None:
    """Print version and exit."""
    if value:
        version = get_safe_version("menv")
        console.print(f"menv version: {version}")
        raise typer.Exit()


app = typer.Typer(
    name="menv",
    help="macOS development environment provisioning CLI.",
    no_args_is_help=True,
)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """menv - Provision and manage your macOS development environment."""


# Register create command and alias
app.command(name="create", help="Provision a macOS development environment.")(create)
app.command(name="cr", help="Provision a macOS development environment.")(create)

# Register update command and alias
app.command(name="update", help="Update menv to the latest version.")(update)
app.command(name="u", help="Update menv to the latest version.")(update)


if __name__ == "__main__":
    app()
