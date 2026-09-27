from relmote import agent_host


def test_detect_agent_host_reports_portable_python_capability(monkeypatch):
    available = {"git", "python", "docker"}

    monkeypatch.setattr(
        agent_host.shutil,
        "which",
        lambda name: f"/tools/{name}" if name in available else None,
    )
    monkeypatch.setattr(agent_host.socket, "gethostname", lambda: "agent-host")
    monkeypatch.setattr(agent_host.platform, "system", lambda: "Windows")
    monkeypatch.setattr(agent_host.platform, "machine", lambda: "AMD64")

    host = agent_host.detect_agent_host()

    assert host.name == "agent-host"
    assert host.platform == "windows"
    assert host.architecture == "AMD64"
    assert "relmote.controller" in host.capabilities
    assert "relmote.agent-client" in host.capabilities
    assert "development.git" in host.capabilities
    assert "development.python" in host.capabilities
    assert "containers" in host.capabilities
    assert host.tools == ("git", "python", "docker")


def test_detect_agent_host_does_not_invent_optional_capabilities(monkeypatch):
    monkeypatch.setattr(agent_host.shutil, "which", lambda name: None)

    host = agent_host.detect_agent_host()

    assert host.capabilities == (
        "relmote.controller",
        "relmote.agent-client",
    )
    assert host.tools == ()
