import pytest

from relmote.software_node import SoftwareNode


def test_ephemeral_node_has_identity_and_no_session():
    node = SoftwareNode()
    snapshot = node.snapshot()

    assert snapshot["node"]["node_id"].startswith("rm:ephemeral:")
    assert snapshot["node"]["fingerprint"]
    assert snapshot["session"] is None


def test_diagnostic_task_requires_observe_session():
    node = SoftwareNode()

    with pytest.raises(PermissionError):
        node.run_task("system-overview")


def test_observe_session_can_run_read_only_task():
    node = SoftwareNode()
    node.start_observe_session()
    task = node.run_task("network-overview")

    assert task.task_type == "network-overview"
    assert {o.capability for o in task.observations} == {
        "system.identify",
        "network.inspect",
    }


def test_revocation_stops_new_tasks():
    node = SoftwareNode()
    node.start_observe_session()
    node.revoke_session()

    with pytest.raises(PermissionError):
        node.run_task("storage-overview")


def test_network_diagnosis_contains_findings_and_evidence():
    node = SoftwareNode()
    node.start_observe_session()
    task = node.run_task("diagnose-network")

    assert task.findings
    assert {o.capability for o in task.observations} == {
        "network.inspect",
        "network.dns",
    }
    assert any(
        finding.status == "not-tested" for finding in task.findings
    )
