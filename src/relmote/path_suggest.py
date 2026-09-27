from __future__ import annotations

from pathlib import Path


def suggest_directories(
    query: str,
    *,
    home: Path | None = None,
    limit: int = 12,
) -> list[str]:
    home = (home or Path.home()).resolve()
    raw = (query or str(home)).strip()
    candidate = Path(raw).expanduser()

    if not candidate.is_absolute():
        candidate = home / candidate

    # Normal autocomplete is intentionally confined to the user's home.
    if raw.endswith("/"):
        parent = candidate
        prefix = ""
    else:
        parent = candidate.parent
        prefix = candidate.name

    try:
        resolved_parent = parent.resolve()
        resolved_parent.relative_to(home)
    except (OSError, ValueError):
        return []

    if not resolved_parent.is_dir():
        return []

    values: list[str] = []
    try:
        children = sorted(
            (p for p in resolved_parent.iterdir() if p.is_dir()),
            key=lambda p: p.name.casefold(),
        )
    except OSError:
        return []

    prefix_folded = prefix.casefold()
    for child in children:
        if prefix_folded and not child.name.casefold().startswith(prefix_folded):
            continue
        try:
            resolved = child.resolve()
            resolved.relative_to(home)
        except (OSError, ValueError):
            continue
        values.append(str(child) + "/")
        if len(values) >= limit:
            break
    return values
