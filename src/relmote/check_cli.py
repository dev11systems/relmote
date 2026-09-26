from __future__ import annotations

import json

from .agent import LocalAgent
from .linux_diagnostics import linux_full_check


def run_check(*, as_json: bool = False) -> int:
    report = linux_full_check(LocalAgent())

    if as_json:
        print(
            json.dumps(
                {
                    "name": report.name,
                    "findings": [
                        {
                            "status": f.status,
                            "statement": f.statement,
                            "evidence": list(f.evidence),
                            "uncertainty": f.uncertainty,
                        }
                        for f in report.findings
                    ],
                    "observations": [
                        {"capability": o.capability, "data": o.data}
                        for o in report.observations
                    ],
                },
                indent=2,
            )
        )
        return 0

    print("RELMOTE — CHECK THIS COMPUTER\n")
    for finding in report.findings:
        marker = {
            "observed": "✓",
            "attention": "!",
            "unknown": "?",
            "not-tested": "○",
        }.get(finding.status, "•")
        print(f"{marker} {finding.statement}")
        if finding.uncertainty:
            print(f"  {finding.uncertainty}")

    attention = sum(1 for f in report.findings if f.status == "attention")
    print()
    if attention:
        print(f"{attention} item(s) may need attention.")
    else:
        print("No attention items were found by the current checks.")
    print("Not-tested items are not treated as passing or failing.")
    return 0
