#!/usr/bin/env python3
"""Delete a git submodule completely."""

from __future__ import annotations

import subprocess
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Delete a git submodule and its metadata.")
console = Console()


def _validate_submodule_path(path: str) -> str:
    submodule_path = Path(path)
    if submodule_path.is_absolute() or ".." in submodule_path.parts:
        console.print(
            f"[bold red]Error[/]: Invalid submodule path '{path}'. Must be a relative path without '..'."
        )
        raise typer.Exit(1)
    return str(submodule_path)


def _run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        console.print(f"[bold red]Error[/]: Command {' '.join(command)} failed: {exc}")
        raise typer.Exit(exc.returncode or 1) from exc


@app.command()
def delete(submodule_path: str = typer.Argument(..., help="Relative path to the submodule.")) -> None:
    """Remove a git submodule, including git metadata."""

    validated = _validate_submodule_path(submodule_path)
    console.print(f"Deleting submodule {validated}...")

    _run(["git", "submodule", "deinit", "-f", validated])
    _run(["git", "rm", "-f", "-r", validated])
    _run(["rm", "-rf", f".git/modules/{validated}"])

    try:
        subprocess.run(
            ["git", "config", "--remove-section", f"submodule.{validated}"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode() if exc.stderr else ""
        if "No such section" not in stderr:
            console.print(
                f"[bold yellow]Warning[/]: Could not remove config section: {stderr.strip()}"
            )

    console.print(f"[bold green]✅[/] Submodule {validated} deleted successfully.")


def main() -> None:  # pragma: no cover - CLI entry
    app()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
