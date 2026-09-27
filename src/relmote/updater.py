from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass

from .version import build_info


REPO_SPEC = "git+https://github.com/dev11systems/relmote.git#egg=relmote[screen-linux]"


@dataclass(frozen=True)
class UpdateStatus:
    current_version: str
    executable: str
    pipx_available: bool
    mode: str


def status() -> UpdateStatus:
    info = build_info()
    return UpdateStatus(
        current_version=info["version"],
        executable=sys.executable,
        pipx_available=shutil.which("pipx") is not None,
        mode=info["channel"],
    )


def update_repo_preview(*, dry_run: bool = False) -> int:
    current = status()
    if not current.pipx_available:
        raise RuntimeError(
            "pipx is not available. Update using the same method used to install Relmote."
        )

    command = ["pipx", "install", "--force", REPO_SPEC]
    if dry_run:
        print("Would update the development preview from:")
        print("  https://github.com/dev11systems/relmote")
        print("Command:")
        print("  " + " ".join(command))
        return 0

    print("Updating Relmote development preview from the repository...")
    completed = subprocess.run(command, check=False)
    if completed.returncode == 0:
        print("Relmote updated. Restart any running Relmote process.")
    return completed.returncode
