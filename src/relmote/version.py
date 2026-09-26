from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version


def package_version() -> str:
    try:
        return version("relmote")
    except PackageNotFoundError:
        return "0.0.1-dev"


def build_info() -> dict[str, str]:
    return {
        "version": package_version(),
        "commit": os.environ.get("RELMOTE_BUILD_COMMIT", "unknown"),
        "channel": os.environ.get("RELMOTE_BUILD_CHANNEL", "development"),
    }
