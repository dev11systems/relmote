from relmote.agent import LocalAgent
from relmote.linux_diagnostics import linux_full_check


def test_full_check_produces_findings_and_evidence():
    report = linux_full_check(LocalAgent())

    assert report.name == "full-check"
    assert report.findings
    assert report.observations
    assert any(
        finding.status == "not-tested" for finding in report.findings
    )


def test_full_check_flags_high_utilization_secondary_mount():
    class HighMountAgent(LocalAgent):
        def _storage(self):
            value = super()._storage()
            value["mounts"] = [
                {
                    "path": "/",
                    "percent_used": 21.0,
                    "total_bytes": 100,
                    "used_bytes": 21,
                    "free_bytes": 79,
                    "fstype": "btrfs",
                },
                {
                    "path": "/mnt/archive",
                    "percent_used": 95.0,
                    "total_bytes": 100,
                    "used_bytes": 95,
                    "free_bytes": 5,
                    "fstype": "ext4",
                },
            ]
            return value

    report = linux_full_check(HighMountAgent())

    assert any(
        finding.status == "attention"
        and "/mnt/archive" in finding.statement
        and "95.0%" in finding.statement
        for finding in report.findings
    )
