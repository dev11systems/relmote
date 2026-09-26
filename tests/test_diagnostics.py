from relmote.agent import AgentObservation
from relmote.diagnostics import diagnose_network


class FakeAgent:
    def __init__(self, network, dns):
        self.values = {
            "network.inspect": AgentObservation("network.inspect", network),
            "network.dns": AgentObservation("network.dns", dns),
        }

    def observe(self, capability):
        return self.values[capability]


def test_diagnosis_does_not_claim_connectivity():
    report = diagnose_network(
        FakeAgent(
            {"addresses": [{"address": "192.0.2.10", "kind": "configured"}]},
            {"servers": ["192.0.2.53"]},
        )
    )

    statements = [x.statement for x in report.findings]
    assert any("configured address" in x for x in statements)
    assert "Internet reachability was not tested." in statements
    assert not any("Internet is working" in x for x in statements)


def test_link_local_is_attention_not_false_dhcp_diagnosis():
    report = diagnose_network(
        FakeAgent(
            {"addresses": [{"address": "169.254.1.2", "kind": "link-local"}]},
            {"servers": []},
        )
    )

    first = report.findings[0]
    assert first.status == "attention"
    assert "DHCP" in first.uncertainty
