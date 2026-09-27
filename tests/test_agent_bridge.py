from pathlib import PurePosixPath

import pytest

from relmote.agent_executor import list_path, read_text, run_command
from relmote.agent_session import AgentCapability, AgentSession
from relmote.agent_bridge import create_grant
from relmote.workspace import WorkspacePolicy


def session_for(tmp_path, *caps):
    policy = WorkspacePolicy.create(
        str(tmp_path),
        allowed_tools=frozenset({"git"}),
    )
    session = AgentSession(
        workspace=policy,
        controller="test-agent",
        capabilities=frozenset(caps),
    )
    session.approve()
    return session


def test_agent_lists_and_reads_only_when_granted(tmp_path):
    (tmp_path / "hello.txt").write_text("hello")
    session = session_for(
        tmp_path,
        AgentCapability.LIST,
        AgentCapability.READ,
    )
    assert list_path(session)[0]["name"] == "hello.txt"
    assert read_text(session, "hello.txt") == "hello"


def test_agent_cannot_escape_workspace(tmp_path):
    session = session_for(tmp_path, AgentCapability.READ)
    with pytest.raises(ValueError):
        read_text(session, "../secret")


def test_agent_exec_requires_allowlisted_tool(tmp_path):
    session = session_for(tmp_path, AgentCapability.EXEC)
    with pytest.raises(PermissionError):
        run_command(session, ["sh", "-c", "echo nope"])


def test_revoked_agent_session_cannot_read(tmp_path):
    (tmp_path / "hello.txt").write_text("hello")
    session = session_for(tmp_path, AgentCapability.READ)
    session.revoke()
    with pytest.raises(PermissionError):
        read_text(session, "hello.txt")


def test_agent_cannot_escape_workspace_through_symlink(tmp_path):
    outside = tmp_path.parent / "outside-secret.txt"
    outside.write_text("secret")
    (tmp_path / "link").symlink_to(outside)
    session = session_for(tmp_path, AgentCapability.READ)
    with pytest.raises(ValueError):
        read_text(session, "link")


def test_agent_token_is_not_in_public_session(tmp_path):
    grant = create_grant(
        str(tmp_path),
        controller="test",
        capabilities=["workspace.read"],
    )
    public = grant.public()

    assert "token" not in public
    assert grant.token not in repr(public)


def test_write_capability_controls_workspace_write_policy(tmp_path):
    readonly = create_grant(
        str(tmp_path),
        controller="test",
        capabilities=["workspace.read"],
    )
    writable = create_grant(
        str(tmp_path),
        controller="test",
        capabilities=["workspace.write"],
    )

    assert readonly.session.workspace.writable is False
    assert writable.session.workspace.writable is True
