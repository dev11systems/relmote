from relmote.agent_host import AgentHost
from relmote.hub_inventory import HubInventory


class FakePairedTargets:
    def __init__(self, *, status_result=None, status_error=None, info_result=None):
        self.status_result = status_result
        self.status_error = status_error
        self.info_result = info_result
        self.status_calls = []
        self.info_calls = []

    def targets(self):
        return [
            {
                "name": "target-a",
                "workspace": "/workspace",
                "state": "active",
                "capabilities": ["workspace.list", "workspace.read"],
            }
        ]

    def status(self, target):
        self.status_calls.append(target)
        if self.status_error is not None:
            raise self.status_error
        return self.status_result or {
            "state": "active",
            "workspace": "/workspace",
            "capabilities": ["workspace.list", "workspace.read"],
        }

    def info(self, target):
        self.info_calls.append(target)
        if self.status_error is not None:
            raise self.status_error
        return self.info_result or {
            "role": "target",
            "target": {"name": "target-node-a"},
            "platform": {"system": "linux", "architecture": "x86_64"},
            "relmote": {
                "display_version": "0.1.0-dev.12",
                "commit": "abcdef1234567890",
                "short_commit": "abcdef12",
                "channel": "repository",
            },
            "session": self.status_result or {
                "state": "active",
                "workspace": "/workspace",
                "capabilities": ["workspace.list", "workspace.read"],
            },
        }


def fake_host():
    return AgentHost(
        name="agent-host-a",
        platform="linux",
        architecture="x86_64",
        capabilities=("relmote.agent-client", "development.codex"),
        tools=("git", "codex"),
    )


def fake_build():
    return {
        "display_version": "0.1.0-dev.12",
        "commit": "abcdef1234567890",
        "short_commit": "abcdef12",
        "channel": "repository",
    }


def test_hub_inventory_is_credential_blind_and_co_located():
    snapshot = HubInventory(
        paired_targets=FakePairedTargets(),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot()

    assert snapshot["hub"] == {
        "role": "hub",
        "mode": "local-read-only",
        "co_located_agent_host": True,
        "authority": "inventory-only",
    }
    assert snapshot["agent_host"]["name"] == "agent-host-a"
    assert snapshot["agent_host"]["relmote"]["short_commit"] == "abcdef12"
    assert snapshot["paired_targets"][0]["role"] == "paired_target"

    text = repr(snapshot)
    assert "token" not in text
    assert "base_url" not in text


def test_hub_live_inventory_reports_active_target():
    service = FakePairedTargets()
    snapshot = HubInventory(
        paired_targets=service,
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    live = snapshot["paired_targets"][0]["live"]
    assert service.info_calls == ["target-a"]
    assert service.status_calls == []
    assert live["reachable"] is True
    assert live["authority"] == "active"
    assert live["state"] == "active"


def test_hub_live_inventory_distinguishes_revoked_from_unreachable():
    denied = HubInventory(
        paired_targets=FakePairedTargets(
            status_error=PermissionError("agent session is not active")
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)["paired_targets"][0]["live"]

    unavailable = HubInventory(
        paired_targets=FakePairedTargets(
            status_error=ConnectionError("connection refused")
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)["paired_targets"][0]["live"]

    assert denied["reachable"] is True
    assert denied["authority"] == "denied"
    assert "not active" in denied["detail"]

    assert unavailable["reachable"] is False
    assert unavailable["authority"] == "unknown"
    assert "connection refused" in unavailable["detail"]


def test_hub_reconciles_revoked_and_stale_credentials_into_attention_states():
    revoked = HubInventory(
        paired_targets=FakePairedTargets(
            status_error=PermissionError(
                "Relmote Agent API: agent session is not active"
            )
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    stale = HubInventory(
        paired_targets=FakePairedTargets(
            status_error=PermissionError(
                "Relmote Agent API: invalid agent session token"
            )
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    revoked_target = revoked["paired_targets"][0]
    assert revoked_target["current"]["health"] == "revoked"
    assert revoked_target["current"]["needs_attention"] is True
    assert "re-pair" in revoked_target["current"]["recommended_action"]
    assert revoked["summary"]["revoked"] == 1
    assert revoked["summary"]["attention"] == 1

    stale_target = stale["paired_targets"][0]
    assert stale_target["current"]["health"] == "stale_credential"
    assert stale_target["current"]["needs_attention"] is True
    assert "re-pair" in stale_target["current"]["recommended_action"]
    assert stale["summary"]["stale_credential"] == 1


def test_hub_summary_counts_active_and_unreachable_targets():
    active = HubInventory(
        paired_targets=FakePairedTargets(),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    unreachable = HubInventory(
        paired_targets=FakePairedTargets(
            status_error=ConnectionError("connection refused")
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    assert active["summary"]["active"] == 1
    assert active["summary"]["attention"] == 0
    assert active["paired_targets"][0]["current"]["health"] == "active"

    assert unreachable["summary"]["unreachable"] == 1
    assert unreachable["summary"]["attention"] == 1
    assert unreachable["paired_targets"][0]["current"]["health"] == "unreachable"


def test_hub_live_inventory_reports_target_build_and_relation():
    same = HubInventory(
        paired_targets=FakePairedTargets(),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    live = same["paired_targets"][0]["live"]
    assert live["target"]["name"] == "target-node-a"
    assert live["platform"] == {"system": "linux", "architecture": "x86_64"}
    assert live["relmote"]["short_commit"] == "abcdef12"
    assert live["build_relation"] == "same_build"
    assert same["summary"]["build_drift"] == 0

    drift = HubInventory(
        paired_targets=FakePairedTargets(
            info_result={
                "role": "target",
                "target": {"name": "target-node-a"},
                "platform": {"system": "linux", "architecture": "x86_64"},
                "relmote": {
                    "display_version": "0.1.0-dev.12",
                    "commit": "9999999999999999",
                    "short_commit": "99999999",
                    "channel": "repository",
                },
                "session": {
                    "state": "active",
                    "workspace": "/workspace",
                    "capabilities": ["workspace.list"],
                },
            }
        ),
        host_factory=fake_host,
        build_factory=fake_build,
    ).snapshot(live=True)

    assert (
        drift["paired_targets"][0]["live"]["build_relation"]
        == "different_build_same_snapshot"
    )
    assert drift["summary"]["build_drift"] == 1
