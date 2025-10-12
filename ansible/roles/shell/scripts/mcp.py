#!/usr/bin/env python3
"""MCP Configuration Management CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import typer
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from rich.console import Console
from rich.table import Table

CONFIG_FILENAME = ".mcp.json"
LOCAL_CONFIG_PATH = Path(CONFIG_FILENAME)
GLOBAL_CONFIG_PATH = Path.home() / CONFIG_FILENAME


class McpServer(BaseModel):
    """Representation of a single MCP server entry."""

    model_config = ConfigDict(extra="allow")

    command: str | None = None
    args: list[str] = Field(default_factory=list)
    description: str | None = None

    def display_command(self) -> str:
        """Return a human-friendly command string."""

        if not self.command:
            return "<missing command>"
        if self.args:
            return f"{self.command} {' '.join(self.args)}"
        return self.command


class McpConfig(BaseModel):
    """Root MCP configuration."""

    model_config = ConfigDict(extra="allow")

    mcpServers: dict[str, McpServer] = Field(default_factory=dict)


app = typer.Typer(help="Manage MCP configuration files.")
console = Console()


def _read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def _load_config(path: Path) -> McpConfig:
    try:
        payload = _read_json(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Configuration not found: {path}") from exc
    try:
        return McpConfig.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid MCP configuration in {path}: {exc}") from exc


def _write_config(path: Path, config: McpConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(config.model_dump(mode="json"), handle, indent=2)
        handle.write("\n")


def _require_global_config() -> Path:
    if not GLOBAL_CONFIG_PATH.exists():
        console.print("[bold red]Error[/]: ~/.mcp.json file not found.")
        raise typer.Exit(1)
    return GLOBAL_CONFIG_PATH


def _require_local_config(suggest_init: bool = False) -> Path:
    if not LOCAL_CONFIG_PATH.exists():
        console.print("[bold red]Error[/]: .mcp.json file not found in current directory.")
        if suggest_init:
            console.print("Run [bold]mcp ini[/] first to create one.")
        raise typer.Exit(1)
    return LOCAL_CONFIG_PATH


def _available_servers_table(config: McpConfig) -> Table:
    table = Table(title="Available MCP servers")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Command", style="magenta")
    table.add_column("Description", style="green")

    for name, server in sorted(config.mcpServers.items()):
        table.add_row(name, server.display_command(), server.description or "—")
    return table


def _load_global_config() -> McpConfig:
    path = _require_global_config()
    try:
        return _load_config(path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[bold red]Error[/]: {exc}")
        raise typer.Exit(1)


def _load_local_config(*, suggest_init: bool = False) -> McpConfig:
    path = _require_local_config(suggest_init=suggest_init)
    try:
        return _load_config(path)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[bold red]Error[/]: {exc}")
        raise typer.Exit(1)


@app.command("ini")
def init_local_config() -> None:
    """Create a new local .mcp.json file."""

    if LOCAL_CONFIG_PATH.exists():
        console.print("[bold red]Error[/]: .mcp.json already exists in the current directory.")
        raise typer.Exit(1)

    _write_config(LOCAL_CONFIG_PATH, McpConfig())
    console.print("[bold green]✅[/] Created .mcp.json with an empty mcpServers map.")


@app.command("ini-f")
def init_from_global() -> None:
    """Copy ~/.mcp.json to the current directory."""

    _require_global_config()
    if LOCAL_CONFIG_PATH.exists():
        console.print("[bold red]Error[/]: .mcp.json already exists in the current directory.")
        raise typer.Exit(1)

    shutil.copy(GLOBAL_CONFIG_PATH, LOCAL_CONFIG_PATH)
    console.print("[bold green]✅[/] Created local .mcp.json from ~/.mcp.json.")


@app.command("ls")
def list_servers() -> None:
    """List available MCP servers."""

    config = _load_global_config()
    if not config.mcpServers:
        console.print("[bold red]Error[/]: No MCP servers found in ~/.mcp.json.")
        raise typer.Exit(1)

    console.print(_available_servers_table(config))


def _normalise_name(name: str) -> str:
    value = name.strip()
    if not value:
        raise typer.BadParameter("MCP server name must not be empty.")
    return value


@app.command("a")
def add_servers(
    names: list[str] = typer.Argument(..., metavar="SERVER", help="Server names to add."),
) -> None:
    """Add servers from ~/.mcp.json into the local configuration."""

    local_config = _load_local_config(suggest_init=True)
    global_config = _load_global_config()

    added_any = False
    for raw_name in names:
        name = _normalise_name(raw_name)

        if name not in global_config.mcpServers:
            console.print(
                f"[bold red]Error[/]: MCP server '{name}' not found in ~/.mcp.json."
            )
            console.print(_available_servers_table(global_config))
            continue

        if name in local_config.mcpServers:
            console.print(
                f"[bold yellow]Warning[/]: MCP server '{name}' already exists locally. Skipping."
            )
            continue

        local_config.mcpServers[name] = global_config.mcpServers[name].model_copy(deep=True)
        console.print(f"[bold green]✅[/] Added MCP server '{name}' to local .mcp.json.")
        added_any = True

    if added_any:
        _write_config(LOCAL_CONFIG_PATH, local_config)


@app.command("rm")
def remove_server(
    name: str = typer.Argument(..., metavar="SERVER", help="Server name to remove."),
) -> None:
    """Remove a server from the local configuration."""

    local_config = _load_local_config()
    key = _normalise_name(name)

    if key not in local_config.mcpServers:
        console.print(
            f"[bold red]Error[/]: MCP server '{key}' not found in local .mcp.json."
        )
        console.print(_available_servers_table(local_config))
        raise typer.Exit(1)

    del local_config.mcpServers[key]
    _write_config(LOCAL_CONFIG_PATH, local_config)
    console.print(f"[bold green]✅[/] Removed MCP server '{key}' from local .mcp.json.")


@app.command("cmd")
def show_command(
    name: str = typer.Argument(..., metavar="SERVER", help="Server name to inspect."),
) -> None:
    """Show and copy the launch command for a server."""

    global_config = _load_global_config()
    key = _normalise_name(name)

    server = global_config.mcpServers.get(key)
    if not server:
        console.print(
            f"[bold red]Error[/]: MCP server '{key}' not found in ~/.mcp.json."
        )
        console.print(_available_servers_table(global_config))
        raise typer.Exit(1)

    command = server.command
    if not command:
        console.print(
            f"[bold red]Error[/]: MCP server '{key}' does not define a command."
        )
        raise typer.Exit(1)

    formatted = server.display_command()
    console.print(f"Command for '{key}': [bold]{formatted}[/]")

    add_format = f"{key} {formatted}"
    try:
        subprocess.run(["pbcopy"], input=add_format.encode(), check=True)
        console.print(f"[bold green]📋[/] Copied to clipboard: {add_format}")
    except subprocess.CalledProcessError:
        console.print("[bold red]Error[/]: Failed to copy command to clipboard.")


def main() -> None:  # pragma: no cover - CLI entry
    app()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
