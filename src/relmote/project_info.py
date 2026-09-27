from __future__ import annotations

PROJECT_NAME = "Relmote"
PROJECT_URL = "https://github.com/dev11systems/relmote"
ISSUES_URL = "https://github.com/dev11systems/relmote/issues"
CHANGELOG_URL = "https://github.com/dev11systems/relmote/blob/main/CHANGELOG.md"

SNAPSHOT_CHANGELOG = """Relmote 0.1.0-dev.5

Screen Observe
- Added explicit screen-observe request and approval sessions.
- Verified Wayland graphical-session and ScreenCast portal readiness.
- Added consent-preserving GNOME ScreenCast portal flow foundations.
- Added asynchronous OS-consent handling so the web controller remains responsive.
- Screen observation and screen control remain separate permissions.

Web/UX
- Added the active Relmote version beside the wordmark.
- Screen request state and portal failures are surfaced to the controller.
- Browser terminal capability status now reflects the implemented terminal.

Previous snapshot: 0.1.0-dev.4

Relmote 0.1.0-dev.4

Terminal
- Browser PTY command execution works end-to-end.
- Added first-pass ANSI rendering for readable command output.
- Continued terminal control-sequence cleanup.

Diagnostics
- Full Check includes CPU and uptime.
- Mounted filesystem utilization is inspected and high utilization is flagged.

Web/UX
- Continued mobile/iPad usability improvements.
- About, changelog, source, and issue links are built in.

Previous snapshot: 0.1.0-dev.3

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
