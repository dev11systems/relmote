from __future__ import annotations

PROJECT_NAME = "Relmote"
PROJECT_URL = "https://github.com/dev11systems/relmote"
ISSUES_URL = "https://github.com/dev11systems/relmote/issues"
CHANGELOG_URL = "https://github.com/dev11systems/relmote/blob/main/CHANGELOG.md"

SNAPSHOT_CHANGELOG = """Relmote 0.1.0-dev.3

Web/UX
- Reworked navigation and mobile/iPad usability.
- Added visible action/error feedback.
- Improved scrollable output/evidence areas.
- Clarified capabilities and remote-access status.

Terminal
- Repaired approval failure handling.
- Terminal startup failures are now visible.
- Administrative terminal remains unavailable.

Diagnostics
- Added readable focused-check summaries.
- Expanded Full Check system detail.

Previous snapshot: 0.1.0-dev.2
- First coherent Fedora/Tailscale web preview.
- Doctor, Full Check, TUI/web shared runtime.
- Automatic Tailscale-only binding with localhost fallback.
- Initial terminal/PTTY preview and shared help.
"""


def bundled_changelog() -> str:
    return SNAPSHOT_CHANGELOG
