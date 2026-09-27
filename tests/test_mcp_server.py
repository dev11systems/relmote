import asyncio

import pytest

pytest.importorskip("mcp")

from relmote.mcp_server import (
    RELMOTE_MCP_INSTRUCTIONS,
    RelmoteMCPTools,
    build_mcp_server,
)


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

    targets = tools.targets()
    assert targets["context"]["this_process_role"] == "agent_host"
    assert targets["targets"][0]["name"] == "target-a"
    assert targets["targets"][0]["role"] == "paired_target"
    assert targets["targets"][0]["workspace_location"] == "target"

    status = tools.status("target-a")
    assert status["ok"] is True
    assert status["context"]["target_role"] == "paired_target"
    assert status["context"]["execution_location"] == "target"
    assert status["target_status"]["state"] == "active"

    listed = tools.list("target-a", "src")
    assert listed["ok"] is True
    assert listed["context"]["path_location"] == "target_workspace"
    assert listed["entries"][0]["name"] == "README.md"

    read = tools.read("target-a", "README.md")
    assert read["ok"] is True
    assert read["context"]["path_location"] == "target_workspace"
    assert read["text"] == "hello\n"

    assert service.calls == [
        ("targets",),
        ("status", "target-a"),
        ("list", "target-a", "src"),
        ("read", "target-a", "README.md"),
    ]


def test_mcp_exec_maps_named_operations_not_arbitrary_git_arguments():
    service = FakeService()
    tools = RelmoteMCPTools(service)

    status_result = tools.exec("target-a", "git_status")
    diff_result = tools.exec("target-a", "git_diff", cwd="src", timeout=12)
    pytest_result = tools.exec("target-a", "pytest", args=["-q"])

    for value in (status_result, diff_result, pytest_result):
        assert value["ok"] is True
        assert value["context"]["execution_location"] == "target"
        assert value["context"]["cwd_location"] == "target_workspace"
        assert value["result"]["returncode"] == 0

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
        "relmote_context",
        "relmote_targets",
        "relmote_target_status",
        "relmote_list",
        "relmote_read",
        "relmote_exec",
    }


def test_mcp_server_declares_host_target_role_instructions():
    server = build_mcp_server(FakeService())

    assert server.instructions == RELMOTE_MCP_INSTRUCTIONS
    assert "Agent Host" in server.instructions
    assert "paired Relmote Target" in server.instructions
    assert "not to the Agent Host filesystem" in server.instructions
    assert "do not bypass" in server.instructions.lower()


def test_context_tool_makes_execution_location_explicit():
    value = RelmoteMCPTools.context()

    assert value["this_process_role"] == "agent_host"
    assert value["target_argument_role"] == "paired_target"
    assert value["target_paths_belong_to"] == "target_workspace"
    assert value["target_execution_location"] == "target"
    assert value["agent_host_filesystem_exposed_as_target"] is False


class DenyingService(FakeService):
    def status(self, target):
        raise PermissionError("agent session is not active")

    def list(self, target, path="."):
        raise ConnectionError("Relmote Agent API unavailable: connection refused")

    def read(self, target, path):
        raise ValueError("workspace path escapes configured root")

    def exec(self, target, argv, *, cwd=".", timeout=30):
        raise PermissionError(
            "Relmote Agent API: agent capability not granted: terminal.exec"
        )


def test_expected_target_failures_are_structured_not_opaque_mcp_errors():
    tools = RelmoteMCPTools(DenyingService())

    status = tools.status("target-a")
    assert status["ok"] is False
    assert status["error"] == {
        "kind": "denied",
        "message": "agent session is not active",
    }

    listed = tools.list("target-a", ".")
    assert listed["ok"] is False
    assert listed["error"]["kind"] == "unavailable"
    assert "connection refused" in listed["error"]["message"]

    read = tools.read("target-a", "../secret")
    assert read["ok"] is False
    assert read["error"]["kind"] == "invalid_request"
    assert "escapes configured root" in read["error"]["message"]

    executed = tools.exec("target-a", "git_status")
    assert executed["ok"] is False
    assert executed["error"]["kind"] == "denied"
    assert "terminal.exec" in executed["error"]["message"]
    assert executed["context"]["execution_location"] == "target"
