#!/usr/bin/env python3
"""Manage SSH keys and per-host configuration snippets."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

VALID_KEY_TYPES = ("ed25519", "rsa", "ecdsa")
HOST_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")

app = typer.Typer(help="Manage SSH keys and per-host configuration snippets.")
console = Console()


def _home() -> Path:
    return Path(os.environ.get("HOME", str(Path.home())))


def _ssh_dir() -> Path:
    return _home() / ".ssh"


def _conf_dir() -> Path:
    return _ssh_dir() / "conf.d"


def _run_ssh_keygen(key_type: str, key_path: Path, host: str) -> None:
    subprocess.run(
        [
            "ssh-keygen",
            "-q",
            "-t",
            key_type,
            "-f",
            str(key_path),
            "-C",
            host,
            "-N",
            "",
        ],
        check=True,
    )


def _write_host_config(host: str, key_type: str, config_path: Path) -> None:
    content = (
        f"Host {host}\n"
        f"  HostName {host}\n"
        "  User git\n"
        f"  IdentityFile ~/.ssh/id_{key_type}_{host}\n"
        "  IdentitiesOnly yes\n"
    )
    config_path.write_text(content)
    os.chmod(config_path, 0o600)


def _validate_host(host: str) -> None:
    if not HOST_PATTERN.fullmatch(host):
        console.print(
            f"[bold red]Error[/]: Invalid host '{host}' (allowed: [A-Za-z0-9._-]+)."
        )
        raise typer.Exit(1)


def _ensure_new_paths(*paths: Path) -> None:
    for path in paths:
        if path.exists():
            console.print(
                f"[bold red]Error[/]: {path} already exists. Refusing to overwrite."
            )
            raise typer.Exit(1)


@app.command("gk")
def generate_key(
    key_type: str = typer.Argument(..., help="SSH key type", metavar="TYPE"),
    host: str = typer.Argument(..., help="Host alias", metavar="HOST"),
) -> None:
    """Generate a key and config snippet for a host."""

    normalized_type = key_type.lower()
    if normalized_type not in VALID_KEY_TYPES:
        console.print(
            "[bold red]Error[/]: Unsupported key type '",
            normalized_type,
            "' (allowed: ",
            "|".join(VALID_KEY_TYPES),
            ").",
            sep="",
        )
        raise typer.Exit(1)

    _validate_host(host)

    ssh_dir = _ssh_dir()
    conf_dir = _conf_dir()
    ssh_dir.mkdir(parents=True, exist_ok=True)
    conf_dir.mkdir(parents=True, exist_ok=True)

    key_path = ssh_dir / f"id_{normalized_type}_{host}"
    pub_key_path = Path(str(key_path) + ".pub")
    config_path = conf_dir / f"{host}.conf"

    _ensure_new_paths(key_path, pub_key_path, config_path)

    _run_ssh_keygen(normalized_type, key_path, host)
    _write_host_config(host, normalized_type, config_path)

    console.print(f"[bold green]✅[/] SSH key and config for '{host}' created.")
    if pub_key_path.exists():
        console.print("[bold]🔑 Public key:[/]")
        console.print(pub_key_path.read_text().strip())


@app.command("ls")
def list_hosts() -> None:
    """List configured hosts."""

    conf_dir = _conf_dir()
    if not conf_dir.exists():
        console.print("[italic]No SSH hosts configured yet.[/]")
        return

    table = Table(title="SSH Hosts", show_lines=False)
    table.add_column("Host", justify="left", style="cyan", no_wrap=True)

    for conf_file in sorted(conf_dir.glob("*.conf")):
        table.add_row(conf_file.stem)

    console.print(table)


@app.command("rm")
def remove_host(
    host: str = typer.Argument(..., help="Host alias to remove", metavar="HOST"),
) -> None:
    """Remove a host configuration and associated keys."""

    _validate_host(host)
    config_path = _conf_dir() / f"{host}.conf"

    if not config_path.exists():
        console.print(f"[bold red]Error[/]: Config for host '{host}' not found.")
        raise typer.Exit(1)

    identity_file: Path | None = None
    for line in config_path.read_text().splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("identityfile"):
            parts = stripped.split(None, 1)
            if len(parts) == 2:
                identity_file = Path(parts[1]).expanduser()
            break

    if identity_file:
        priv_path = identity_file
        pub_path = Path(str(identity_file) + ".pub")
        for path in (priv_path, pub_path):
            if path.exists():
                path.unlink()
        console.print(f"[bold yellow]🗑️[/] Removed key files for {host}.")

    config_path.unlink()
    console.print(f"[bold yellow]🗑️[/] Removed config file for '{host}'.")


def main() -> None:  # pragma: no cover - CLI entry
    app()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
