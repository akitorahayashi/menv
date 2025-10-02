from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest
import yaml


@pytest.mark.parametrize(
    ("role", "task_name"),
    [
        ("coderabbit", "Download CodeRabbit CLI installer"),
        ("cursor", "Download Cursor CLI installer"),
    ],
)
def test_cli_install_script_checksum_matches(project_root: Path, role: str, task_name: str) -> None:
    """Ensure installer checksums match the published script contents."""
    tasks_file = project_root / "ansible" / "roles" / role / "tasks" / "main.yml"
    with tasks_file.open(encoding="utf-8") as file:
        tasks = yaml.safe_load(file)

    download_task = next((task for task in tasks if task.get("name") == task_name), None)
    assert download_task, f"Could not find installer download task for role '{role}'."

    get_url_task = download_task.get("ansible.builtin.get_url") or download_task.get("get_url")
    assert get_url_task, f"Task '{task_name}' for role '{role}' is not a 'get_url' task."

    checksum = get_url_task.get("checksum")
    assert checksum, f"Expected checksum to be defined for role '{role}'."

    algorithm, _, digest = checksum.partition(":")
    assert algorithm == "sha256", "Only sha256 checksums are supported."
    assert digest, "Checksum digest must not be empty."

    url = get_url_task.get("url")
    assert url, f"Expected download URL to be defined for role '{role}'."

    try:
        with urlopen(url, timeout=30) as response:
            content = response.read()
    except URLError as exc:  # pragma: no cover - skip when network is unavailable
        pytest.skip(f"Unable to download {url!r} to verify checksum: {exc}")

    computed_digest = hashlib.sha256(content).hexdigest()
    assert (
        computed_digest == digest
    ), f"Checksum mismatch for {role}: expected {digest}, got {computed_digest}"
