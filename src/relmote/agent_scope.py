from __future__ import annotations

from pathlib import Path


def classify_scope(root: str) -> dict:
    path = Path(root).expanduser()
    text = str(path)

    if text == "/":
        return {
            "level": "extreme",
            "label": "Filesystem root",
            "message": "This grant can expose the entire filesystem readable by the Relmote user.",
        }

    if text == "/home":
        return {
            "level": "high",
            "label": "Multiple-user home root",
            "message": "This grant may expose multiple users' readable home-directory contents.",
        }

    parts = path.parts
    if len(parts) == 3 and parts[:2] == ("/", "home"):
        return {
            "level": "medium",
            "label": "Whole home directory",
            "message": "This grant covers the user's entire home directory rather than one project.",
        }

    return {
        "level": "normal",
        "label": "Scoped workspace",
        "message": "This looks like a specific workspace scope.",
    }
