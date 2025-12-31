"""Code command to open current directory in VS Code."""

import shutil
import subprocess

import typer
from rich.console import Console

console = Console()


def code() -> None:
    """Open current directory in VS Code.

    Opens the current working directory in Visual Studio Code using the
    'code' command-line tool. If the tool is not installed, displays
    installation instructions.

    Examples:
        menv code

    Raises:
        typer.Exit: If the 'code' command is not found in PATH.
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

    try:
        result = subprocess.run(["code", "."], check=True, capture_output=True)
        if result.returncode == 0:
            console.print("[dim]✓ Opened current directory in VS Code[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error:[/] Failed to open VS Code: {e}")
        raise typer.Exit(code=1)
