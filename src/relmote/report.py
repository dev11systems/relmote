from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .software_node import SoftwareNode


def export_support_report(node: SoftwareNode, destination: str | Path) -> Path:
    """Export current in-memory preview state.

    The preview report intentionally contains diagnostic observations and node
    metadata. Users should inspect it before sharing because hostnames,
    addresses, storage sizes, and similar machine information may be present.
    """

    path = Path(destination)
    value = {
        "format": "relmote-support-report-v0",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "warning": (
            "Inspect before sharing: this report may contain hostnames, "
            "network addresses, and other machine metadata."
        ),
        "state": node.snapshot(),
    }
    path.write_text(json.dumps(value, indent=2, default=str) + "\n")
    return path
