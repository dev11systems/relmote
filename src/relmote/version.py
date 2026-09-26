from __future__ import annotations

import json
import os
from importlib.metadata import PackageNotFoundError, distribution, version


def package_version() -> str:
    try:
        return version("relmote")
    except PackageNotFoundError:
        return "0.0.1-dev"


def installed_vcs_commit() -> str | None:
    """Return the commit recorded by a PEP 610 VCS install, when available."""
    try:
        dist = distribution("relmote")
    except PackageNotFoundError:
        return None

    raw = dist.read_text("direct_url.json")
    if not raw:
        return None

    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None

    commit = value.get("vcs_info", {}).get("commit_id")
    return commit if isinstance(commit, str) and commit else None


def build_info() -> dict[str, str]:
    commit = (
        os.environ.get("RELMOTE_BUILD_COMMIT")
        or installed_vcs_commit()
        or "unknown"
    )
    channel = os.environ.get("RELMOTE_BUILD_CHANNEL")
    if not channel:
        channel = "repository" if installed_vcs_commit() else "development"

    return {
        "version": package_version(),
        "commit": commit,
        "channel": channel,
    }
