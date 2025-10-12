#!/usr/bin/env python3
"""CLI wrapper for invoking aider with Ollama models."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

import typer
from rich.console import Console

MODEL_ENV = "AIDER_OLLAMA_MODEL"

app = typer.Typer(
    add_completion=False,
    help="Invoke aider with curated defaults for the Environment setup project.",
)
console = Console()


def _iter_extension_matches(extensions: Iterable[str]) -> Iterable[str]:
    cwd = Path.cwd()
    for ext in extensions:
        normalized = ext.lstrip(".")
        if not normalized:
            continue
        for path in sorted(cwd.rglob(f"*.{normalized}")):
            if path.is_file():
                try:
                    yield str(path.relative_to(cwd))
                except ValueError:
                    yield str(path)


def _build_aider_command(
    *,
    directories: Sequence[Path],
    extensions: Sequence[str],
    files: Sequence[Path],
    yolo: bool,
    message: str | None,
    targets: Sequence[Path],
) -> list[str]:
    model = os.getenv(MODEL_ENV)
    if not model:
        console.print(
            f"[bold red]Error[/]: {MODEL_ENV} environment variable is not set. Use `ai set-model <model>` to set it."
        )
        raise typer.Exit(1)

    provider_model = model if "/" in model else f"ollama/{model}"

    command: list[str] = [
        "aider",
        "--model",
        provider_model,
        "--no-auto-commit",
        "--no-gitignore",
    ]

    if yolo:
        command.append("--yes")

    if message:
        command.extend(["--message", message])

    target_args: list[str] = []
    target_args.extend(str(path) for path in directories)
    target_args.extend(_iter_extension_matches(extensions))
    target_args.extend(str(path) for path in files)
    target_args.extend(str(path) for path in targets)

    return command + target_args


def _run_aider(command: list[str]) -> int:
    try:
        completed = subprocess.run(command, check=False)
    except FileNotFoundError as exc:  # pragma: no cover - defensive guard
        console.print(f"[bold red]Error[/]: failed to execute {command[0]!r}: {exc}")
        return 1
    return completed.returncode


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    directories: tuple[Path, ...] = typer.Option(
        (),
        "--dir",
        "-d",
        help="Add a directory (recursively) to the aider context.",
        metavar="DIR",
    ),
    extensions: tuple[str, ...] = typer.Option(
        (),
        "--ext",
        "-e",
        help="Add files by extension (recursively).",
        metavar="EXT",
    ),
    files: tuple[Path, ...] = typer.Option(
        (),
        "--file",
        "--files",
        "-f",
        help="Add specific files to the aider context. Repeat for multiple files.",
        metavar="FILE",
    ),
    yolo: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Automatically accept aider suggestions (YOLO mode).",
    ),
    message: str | None = typer.Option(
        None,
        "--message",
        "-m",
        help="Send a one-off message to aider before exiting.",
        metavar="TEXT",
    ),
    targets: tuple[Path, ...] = typer.Argument(
        (),
        metavar="TARGET",
        help="Additional files or directories to include.",
    ),
) -> None:
    """Default aider invocation."""

    if ctx.invoked_subcommand is not None:
        return

    command = _build_aider_command(
        directories=directories,
        extensions=extensions,
        files=files,
        yolo=yolo,
        message=message,
        targets=targets,
    )
    raise typer.Exit(_run_aider(command))


@app.command("set-model")
def set_model(
    model: str = typer.Argument(..., metavar="MODEL", help="Default Ollama model."),
) -> None:
    """Print shell commands to set the default Ollama model for aider."""

    quoted = shlex.quote(model)
    console.print(f"export {MODEL_ENV}={quoted}")
    console.print(f'echo "✅ Set {MODEL_ENV} to: {model}"')


@app.command("unset-model")
def unset_model() -> None:
    """Print shell commands to unset the configured Ollama model."""

    if os.getenv(MODEL_ENV):
        console.print(f"unset {MODEL_ENV}")
        console.print(f'echo "✅ Unset {MODEL_ENV}"')
    else:
        console.print(f'echo "{MODEL_ENV} is already not set"')


@app.command("list-models")
def list_models() -> None:
    """List available Ollama models."""

    if not shutil.which("ollama"):
        console.print("[bold red]Error[/]: Ollama is not installed.")
        raise typer.Exit(1)

    try:
        result = subprocess.run(
            ["ollama", "list"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover - passthrough
        console.print(exc.stderr or str(exc))
        raise typer.Exit(exc.returncode or 1)

    models: list[str] = []
    for idx, line in enumerate(result.stdout.splitlines()):
        if idx == 0 and line.lower().startswith("name"):
            continue
        parts = line.split()
        if parts:
            models.append(parts[0])

    console.print("Available Ollama models for aider:")
    for name in models:
        console.print(f"  {name}")
    console.print()
    console.print("Usage: ai set-model <model> && ai [files...]")
    console.print("Example: ai set-model llama3.2 && ai main.py")
    console.print()
    current = os.getenv(MODEL_ENV, "not set")
    console.print(f"Current {MODEL_ENV}: {current}")


def run() -> None:  # pragma: no cover - CLI entry
    app()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    run()
