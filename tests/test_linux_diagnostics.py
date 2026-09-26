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
