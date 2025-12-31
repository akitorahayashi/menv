"""Collect brew dependencies from all roles."""

from __future__ import annotations

import re
from pathlib import Path


def collect_formulae(roles_dir: Path) -> list[str]:
    """Collect all brew formulae from role task files.

    Scans platform.yml and main.yml files in each role for homebrew
    install tasks and extracts the formula names.

    Args:
        roles_dir: Path to the ansible roles directory.

    Returns:
        Deduplicated list of formula names.
    """
    formulae: list[str] = []

    for role_dir in roles_dir.iterdir():
        if not role_dir.is_dir():
            continue

        tasks_dir = role_dir / "tasks"
        if not tasks_dir.exists():
            continue

        # Check platform.yml first (language runtimes), then main.yml
        for task_file in ["platform.yml", "main.yml"]:
            task_path = tasks_dir / task_file
            if task_path.exists():
                formulae.extend(_extract_formulae(task_path))

    # Deduplicate while preserving order
    return list(dict.fromkeys(formulae))


def _extract_formulae(task_file: Path) -> list[str]:
    """Extract brew formula names from a task file.

    Args:
        task_file: Path to the Ansible task file.

    Returns:
        List of formula names found in the file.
    """
    formulae: list[str] = []
    content = task_file.read_text()

    # Pattern for single formula: name: formula_name
    single_pattern = re.compile(
        r"community\.general\.homebrew:\s*\n\s*name:\s*(\w[\w-]*)",
        re.MULTILINE,
    )
    for match in single_pattern.finditer(content):
        formulae.append(match.group(1))

    # Pattern for loop items: - formula_name
    loop_pattern = re.compile(
        r"community\.general\.homebrew:.*?\n\s*name:.*?\n\s*state:.*?\n\s*loop:\s*\n((?:\s*-\s*\w[\w-]*\n?)+)",
        re.MULTILINE | re.DOTALL,
    )
    for match in loop_pattern.finditer(content):
        items_block = match.group(1)
        item_pattern = re.compile(r"-\s*(\w[\w-]*)")
        for item_match in item_pattern.finditer(items_block):
            formulae.append(item_match.group(1))

    return formulae
