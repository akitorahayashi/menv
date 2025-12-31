"""Code command to open menv source code in VS Code."""

import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console

console = Console()


def find_menv_root() -> Path | None:
    """Find the menv project root directory.

    Searches for the project root by traversing up from the current module
    location until finding a directory containing pyproject.toml.

    Returns:
        Path to menv project root, or None if not found.
    """
    current = Path(__file__).resolve()

    # Traverse up to find pyproject.toml
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            # Verify it's the menv project
            pyproject = parent / "pyproject.toml"
            if pyproject.read_text().find('name = "menv"') != -1:
                return parent

    return None


def code() -> None:
    """Open menv source code in VS Code.

    Opens the menv project source directory in Visual Studio Code. This allows
    you to edit the menv codebase directly from the pipx installation without
    needing to clone the repository separately.

    Examples:
        menv code

    Raises:
        typer.Exit: If the 'code' command is not found or menv root cannot be located.
    """
    if not shutil.which("code"):
        console.print(
            "[bold red]Error:[/] The 'code' command was not found in your PATH."
        )
        console.print(
            "Hint: In VS Code, open the Command Palette (Cmd+Shift+P) and run "
            "'Shell Command: Install 'code' command in PATH'."
        )
        raise typer.Exit(code=1)

    menv_root = find_menv_root()
    if not menv_root:
        console.print(
            "[bold red]Error:[/] Could not locate menv project root directory."
        )
        raise typer.Exit(code=1)

    try:
        result = subprocess.run(
            ["code", str(menv_root)], check=True, capture_output=True
        )
        if result.returncode == 0:
            console.print(
                f"[dim]✓ Opened menv project in VS Code[/] [dim cyan]({menv_root})[/]"
            )
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/] Failed to open VS Code: {e}")
        raise typer.Exit(code=1)
