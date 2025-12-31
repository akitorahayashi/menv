"""Fixtures for core module tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def mock_roles_dir(tmp_path: Path) -> Path:
    """Create a mock roles directory with sample task files.

    Args:
        tmp_path: pytest's temporary directory fixture.

    Returns:
        Path to the mock roles directory.
    """
    roles_dir = tmp_path / "roles"
    roles_dir.mkdir()

    # Create a python role with platform.yml containing brew formulae
    python_tasks = roles_dir / "python" / "tasks"
    python_tasks.mkdir(parents=True)
    (python_tasks / "platform.yml").write_text(
        """---
- name: "Install pyenv"
  community.general.homebrew:
    name: pyenv
    state: present
"""
    )

    # Create a nodejs role with loop-style brew formulae
    nodejs_tasks = roles_dir / "nodejs" / "tasks"
    nodejs_tasks.mkdir(parents=True)
    (nodejs_tasks / "platform.yml").write_text(
        """---
- name: "Install nvm, jq, and pnpm"
  community.general.homebrew:
    name: "{{ item }}"
    state: present
  loop:
    - nvm
    - jq
    - pnpm
"""
    )

    # Create a role without brew tasks
    shell_tasks = roles_dir / "shell" / "tasks"
    shell_tasks.mkdir(parents=True)
    (shell_tasks / "main.yml").write_text(
        """---
- name: "Symlink .zshrc"
  ansible.builtin.file:
    src: "{{ role_path }}/config/common/.zshrc"
    dest: "{{ ansible_env.HOME }}/.zshrc"
    state: link
"""
    )

    return roles_dir
