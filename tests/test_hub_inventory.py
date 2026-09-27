from relmote.agent_host import AgentHost
from relmote.hub_inventory import HubInventory


class FakePairedTargets:
    def __init__(self, *, status_result=None, status_error=None):
        self.status_result = status_result
        self.status_error = status_error
        self.status_calls = []

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
    assert service.status_calls == ["target-a"]
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
