import asyncio

import pytest

pytest.importorskip("mcp")

from relmote.mcp_server import RelmoteMCPTools, build_mcp_server


class FakeService:
    def __init__(self):
        self.calls = []

    def targets(self):
        self.calls.append(("targets",))
        return [
            {
                "name": "target-a",
                "workspace": "/workspace",
                "state": "active",
                "capabilities": ["workspace.list", "workspace.read"],
            }
        ]

    def status(self, target):
        self.calls.append(("status", target))
        return {"state": "active", "workspace": "/workspace"}

    def list(self, target, path="."):
        self.calls.append(("list", target, path))
        return [{"name": "README.md", "type": "file", "size": 5}]

    def read(self, target, path):
        self.calls.append(("read", target, path))
        return "hello\n"

    def exec(self, target, argv, *, cwd=".", timeout=30):
        self.calls.append(("exec", target, argv, cwd, timeout))
        return {"returncode": 0, "stdout": "ok\n", "stderr": ""}


def test_mcp_tools_reuse_paired_target_service_boundary():
    service = FakeService()
    tools = RelmoteMCPTools(service)

    assert tools.targets()[0]["name"] == "target-a"
    assert tools.status("target-a")["state"] == "active"
    assert tools.list("target-a", "src")[0]["name"] == "README.md"
    assert tools.read("target-a", "README.md") == "hello\n"

    assert service.calls == [
        ("targets",),
        ("status", "target-a"),
        ("list", "target-a", "src"),
        ("read", "target-a", "README.md"),
    ]


def test_mcp_exec_maps_named_operations_not_arbitrary_git_arguments():
    service = FakeService()
    tools = RelmoteMCPTools(service)

    tools.exec("target-a", "git_status")
    tools.exec("target-a", "git_diff", cwd="src", timeout=12)
    tools.exec("target-a", "pytest", args=["-q"])

    assert service.calls == [
        ("exec", "target-a", ["git", "status"], ".", 30),
        ("exec", "target-a", ["git", "diff"], "src", 12),
        ("exec", "target-a", ["pytest", "-q"], ".", 30),
    ]

    with pytest.raises(ValueError, match="does not accept extra arguments"):
        tools.exec("target-a", "git_status", args=["--porcelain"])


def test_mcp_server_exposes_only_initial_agent_host_tools():
    server = build_mcp_server(FakeService())

    tool_list = asyncio.run(server.list_tools())
    names = {tool.name for tool in tool_list}

    assert names == {
        "relmote_targets",
        "relmote_target_status",
        "relmote_list",
        "relmote_read",
        "relmote_exec",
    }
