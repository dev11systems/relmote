import pytest

from relmote.workspace import WorkspacePolicy


def test_workspace_requires_absolute_remote_root():
    with pytest.raises(ValueError):
        WorkspacePolicy.create("relative/project")


def test_workspace_confines_relative_paths():
    policy = WorkspacePolicy.create("/home/user/project")

    assert str(policy.resolve_relative("src/main.py")) == "/home/user/project/src/main.py"

    with pytest.raises(ValueError, match="escapes"):
        policy.resolve_relative("../../.ssh/id_ed25519")

    with pytest.raises(ValueError, match="relative"):
        policy.resolve_relative("/etc/passwd")


def test_workspace_is_read_only_by_default():
    policy = WorkspacePolicy.create("/home/user/project")

    with pytest.raises(PermissionError, match="read-only"):
        policy.require_write()


def test_tool_allowlist():
    policy = WorkspacePolicy.create("/home/user/project")

    policy.require_tool("git")
    with pytest.raises(PermissionError):
        policy.require_tool("bash")
