from relmote.agent import LocalAgent


def test_s1_agent_is_read_only_capability_set():
    agent = LocalAgent()

    assert "system.identify" in agent.capabilities
    assert "network.inspect" in agent.capabilities
    assert not any(cap.endswith(".write") for cap in agent.capabilities)
    assert "shell.write" not in agent.capabilities


def test_snapshot_contains_real_observations():
    value = LocalAgent().snapshot()

    assert value["observations"]["system.identify"]["hostname"]
    assert value["observations"]["system.platform"]["system"]
    assert value["observations"]["storage.inspect"]["total_bytes"] > 0
