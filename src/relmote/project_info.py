from __future__ import annotations

from pathlib import Path

PROJECT_NAME = "Relmote"
PROJECT_URL = "https://github.com/dev11systems/relmote"
ISSUES_URL = "https://github.com/dev11systems/relmote/issues"
CHANGELOG_URL = "https://github.com/dev11systems/relmote/blob/main/CHANGELOG.md"


def bundled_changelog() -> str:
    candidates = (
        Path(__file__).resolve().parents[2] / "CHANGELOG.md",
        Path(__file__).resolve().parents[1] / "CHANGELOG.md",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    return (
        "The bundled changelog is unavailable in this installation.\n"
        f"View it at: {CHANGELOG_URL}\n"
    )
