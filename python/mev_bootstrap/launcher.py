"""Launcher that delegates to the bundled mev Rust binary.

This module is the sole Python entrypoint exposed via pipx.
It locates the platform-specific mev binary committed in the
bundled_binaries directory and executes it, forwarding all
arguments and exit codes.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path


def _platform_key() -> str:
    """Return the platform directory key (e.g. ``darwin-aarch64``)."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine == "arm64":
        machine = "aarch64"
    return f"{system}-{machine}"


def _locate_binary() -> Path:
    """Locate the bundled ``mev`` binary for the current platform.

    Resolution order:
    1. ``bundled_binaries/<platform>/mev`` relative to this package.
    2. ``src/menv/bundled_binaries/<platform>/mev`` for repository dev mode.

    Raises:
        FileNotFoundError: Binary is missing for this platform.
        PermissionError: Binary exists but is not executable.
    """
    key = _platform_key()
    candidates = [
        # Installed via pipx (hatch force-include places it relative to package root)
        Path(__file__).resolve().parent.parent / "menv" / "bundled_binaries" / key / "mev",
        # Repository development mode (running from source checkout)
        Path(__file__).resolve().parent.parent.parent / "src" / "menv" / "bundled_binaries" / key / "mev",
    ]

    for candidate in candidates:
        if candidate.exists():
            if not os.access(candidate, os.X_OK):
                raise PermissionError(
                    f"Bundled mev binary at {candidate} is not executable. "
                    "Check file permissions."
                )
            return candidate

    searched = "\n  ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"Bundled mev binary not found for platform '{key}'.\n"
        f"Searched:\n  {searched}\n"
        "Run 'just build-bundle' to build and place the binary."
    )


def main() -> None:
    """Entry point: locate and exec the bundled mev binary."""
    try:
        binary = _locate_binary()
    except (FileNotFoundError, PermissionError) as exc:
        print(f"mev-bootstrap: {exc}", file=sys.stderr)
        sys.exit(127)

    result = subprocess.run([str(binary), *sys.argv[1:]], check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
