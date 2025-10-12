#!/usr/bin/env python3
"""Synchronize MCP server configuration into Gemini settings."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError


def _print_error(message: str) -> None:
    print(f"❌ {message}", file=sys.stderr)


def _find_project_root(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / ".mcp.json").exists():
            return path
    raise FileNotFoundError(
        "Unable to locate .mcp.json in current or parent directories"
    )


class McpServer(BaseModel):
    """Representation of an MCP server definition."""

    model_config = ConfigDict(extra="allow")

    command: str | None = None
    args: list[str] = Field(default_factory=list)
    description: str | None = None


class McpConfig(BaseModel):
    """Root MCP configuration."""

    model_config = ConfigDict(extra="allow")

    mcpServers: dict[str, McpServer] = Field(default_factory=dict)


class GeminiSettings(BaseModel):
    """Gemini settings JSON structure."""

    model_config = ConfigDict(extra="allow")

    mcpServers: dict[str, McpServer] = Field(default_factory=dict)


def _read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - exercised via error path tests
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def _parse_config(path: Path) -> McpConfig:
    payload = _read_json(path)
    try:
        return McpConfig.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid MCP configuration in {path}: {exc}") from exc


def _parse_settings(path: Path) -> GeminiSettings:
    payload = _read_json(path)
    try:
        return GeminiSettings.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid Gemini settings in {path}: {exc}") from exc


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def sync_mcp_servers(start_dir: Path) -> tuple[dict[str, McpServer], Path]:
    project_root = _find_project_root(start_dir)
    mcp_path = project_root / ".mcp.json"
    gemini_settings = start_dir / ".gemini" / "settings.json"

    mcp_config = _parse_config(mcp_path)
    servers = mcp_config.mcpServers

    try:
        settings_content = _parse_settings(gemini_settings)
    except FileNotFoundError:
        settings_content = GeminiSettings()

    settings_content.mcpServers = servers
    _write_json(gemini_settings, settings_content.model_dump(mode="json"))
    return servers, gemini_settings


def main() -> int:
    start_dir = Path.cwd()
    try:
        servers, settings_path = sync_mcp_servers(start_dir)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        _print_error(str(exc))
        return 1

    configured = ", ".join(sorted(servers.keys())) if servers else "(none)"
    print(f"✅ Synced MCP servers to {settings_path}")
    print(f"📊 Servers configured: {configured}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
