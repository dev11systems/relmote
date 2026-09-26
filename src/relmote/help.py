from __future__ import annotations

TOPICS: dict[str, str] = {
    "getting-started": """RELMOTE — GETTING STARTED

Common first steps:

  relmote doctor
    Check whether this machine is ready for the preview.

  relmote check
    Run a plain-language system check.

  relmote
    Open the interactive TUI and local web interface.

  relmote update
    Update a development-preview install from the repository.

Use:
  relmote help <topic>

Topics:
  support
  check
  remote
  workspace
  update
  privacy
""",
    "support": """RELMOTE — SUPPORT

Relmote separates installation from support access.

Typical flow:

  relmote
    Open Relmote.

Support can be:
  off
  enabled temporarily
  enabled until you turn it off

Enabling support does not automatically grant every capability.

Use the TUI/web interface to review what a helper can see or do.
""",
    "check": """RELMOTE — CHECK THIS COMPUTER

  relmote check
    Run the full plain-language check.

  relmote check --json
    Emit structured findings and observations.

  relmote diagnose network
    Run a focused network diagnosis.

Relmote distinguishes observed, attention, unknown, and not-tested results.
""",
    "remote": """RELMOTE — REMOTE ACCESS

Relmote can use existing private networking such as Tailscale and SSH.

Examples:

  ssh target relmote check

  relmote ssh probe target hostname

Relmote does not automatically enable SSH or Tailscale.

Remote browser access is being developed around explicit support availability
and authenticated/private-network paths.
""",
    "workspace": """RELMOTE — WORKSPACES

A workspace confines project operations to one configured remote root.

Examples:

  relmote workspace target /path/to/project list
  relmote workspace target /path/to/project read README.md
  relmote workspace target /path/to/project git-status
  relmote workspace target /path/to/project git-diff

The preview rejects path traversal and remote symlink escapes.

Write approval and planner integration are still under active development.
""",
    "update": """RELMOTE — UPDATES

For a repository-installed development preview:

  relmote update --check
    Show what would be updated.

  relmote update
    Refresh Relmote from dev11systems/relmote using pipx.

Restart running Relmote processes after updating.
""",
    "privacy": """RELMOTE — PRIVACY AND SAFETY

Current preview principles:

  • localhost by default
  • no public listener by default
  • no arbitrary shell by default
  • read-only diagnostics first
  • changes require stronger authorization
  • support can be stopped
  • no mandatory cloud account

Diagnostic reports may contain hostnames, network addresses, storage details,
and other machine metadata. Inspect reports before sharing them.
""",
}


def topic_names() -> tuple[str, ...]:
    return tuple(sorted(TOPICS))


def render_help(topic: str | None = None) -> str:
    if topic is None:
        return TOPICS["getting-started"]
    try:
        return TOPICS[topic]
    except KeyError as exc:
        available = ", ".join(topic_names())
        raise ValueError(
            f"unknown help topic: {topic}. Available topics: {available}"
        ) from exc


def print_help_topic(topic: str | None = None) -> int:
    print(render_help(topic))
    return 0
