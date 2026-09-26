from __future__ import annotations

import json

from .agent import LocalAgent
from .diagnostics import diagnose_network


def status() -> int:
    agent = LocalAgent()
    value = {
        "implementation": "software-preview",
        "capabilities": sorted(agent.capabilities),
        "system": agent.observe("system.identify").data,
        "platform": agent.observe("system.platform").data,
    }
    print(json.dumps(value, indent=2))
    return 0


def diagnose(kind: str) -> int:
    agent = LocalAgent()
    if kind != "network":
        raise ValueError(f"unsupported preview diagnosis: {kind}")

    report = diagnose_network(agent)
    print(f"Relmote diagnosis: {report.name}")
    for finding in report.findings:
        print(f"[{finding.status}] {finding.statement}")
        if finding.uncertainty:
            print(f"  {finding.uncertainty}")
    return 0
