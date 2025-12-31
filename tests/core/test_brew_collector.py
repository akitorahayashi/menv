"""Tests for brew_collector module."""

from __future__ import annotations

from pathlib import Path

from menv.core.brew_collector import collect_formulae


class TestCollectFormulae:
    """Tests for collect_formulae function."""

    def test_collects_single_formula(self, mock_roles_dir: Path) -> None:
        """Test that single formula names are collected."""
        formulae = collect_formulae(mock_roles_dir)

        assert "pyenv" in formulae

    def test_collects_loop_formulae(self, mock_roles_dir: Path) -> None:
        """Test that formulae from loop constructs are collected."""
        formulae = collect_formulae(mock_roles_dir)

        assert "nvm" in formulae
        assert "jq" in formulae
        assert "pnpm" in formulae

    def test_deduplicates_formulae(self, tmp_path: Path) -> None:
        """Test that duplicate formulae are removed."""
        roles_dir = tmp_path / "roles"
        roles_dir.mkdir()

        # Create two roles with the same formula
        for role_name in ["role1", "role2"]:
            tasks = roles_dir / role_name / "tasks"
            tasks.mkdir(parents=True)
            (tasks / "platform.yml").write_text(
                """---
- name: "Install git"
  community.general.homebrew:
    name: git
    state: present
"""
            )

        formulae = collect_formulae(roles_dir)

        assert formulae.count("git") == 1

    def test_returns_empty_for_no_brew_tasks(self, tmp_path: Path) -> None:
        """Test that empty list is returned when no brew tasks exist."""
        roles_dir = tmp_path / "roles"
        roles_dir.mkdir()

        # Create a role without any brew tasks
        tasks = roles_dir / "shell" / "tasks"
        tasks.mkdir(parents=True)
        (tasks / "main.yml").write_text(
            """---
- name: "Copy file"
  ansible.builtin.copy:
    src: "source"
    dest: "dest"
"""
        )

        formulae = collect_formulae(roles_dir)

        assert formulae == []

    def test_handles_empty_roles_dir(self, tmp_path: Path) -> None:
        """Test that empty list is returned for empty roles directory."""
        roles_dir = tmp_path / "roles"
        roles_dir.mkdir()

        formulae = collect_formulae(roles_dir)

        assert formulae == []

    def test_skips_non_directory_entries(self, mock_roles_dir: Path) -> None:
        """Test that non-directory entries in roles_dir are skipped."""
        # Create a file in the roles directory
        (mock_roles_dir / "README.md").write_text("# Roles")

        # Should not raise an error
        formulae = collect_formulae(mock_roles_dir)

        assert len(formulae) > 0
