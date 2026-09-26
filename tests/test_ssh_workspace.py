from unittest.mock import patch

import pytest

from relmote.ssh_workspace import SSHWorkspace
from relmote.workspace import WorkspacePolicy


def completed(returncode=0, stdout="", stderr=""):
    value = type("Completed", (), {})()
    value.returncode = returncode
    value.stdout = stdout
    value.stderr = stderr
    return value


@patch("relmote.ssh_workspace.subprocess.run")
def test_read_resolves_remote_path_before_access(mock_run):
    mock_run.side_effect = [
        completed(stdout="/home/user/project/README.md\n"),
        completed(stdout="/home/user/project\n"),
        completed(stdout="hello"),
    ]
    workspace = SSHWorkspace(
        "cousin-host",
        WorkspacePolicy.create("/home/user/project"),
    )

    result = workspace.read("README.md")

    final_argv = mock_run.call_args_list[-1].args[0]
    assert final_argv[-3:] == ["cat", "--", "/home/user/project/README.md"]
    assert result.stdout == "hello"


@patch("relmote.ssh_workspace.subprocess.run")
def test_symlink_escape_is_rejected(mock_run):
    mock_run.side_effect = [
        completed(stdout="/home/user/.ssh/id_ed25519\n"),
        completed(stdout="/home/user/project\n"),
    ]
    workspace = SSHWorkspace(
        "cousin-host",
        WorkspacePolicy.create("/home/user/project"),
    )

    with pytest.raises(PermissionError, match="symlink"):
        workspace.read("link/id_ed25519")


@patch("relmote.ssh_workspace.subprocess.run")
def test_git_status_is_explicit_operation(mock_run):
    mock_run.return_value = completed(stdout=" M README.md\n")
    workspace = SSHWorkspace(
        "cousin-host",
        WorkspacePolicy.create("/home/user/project"),
    )

    result = workspace.git_status()

    argv = mock_run.call_args.args[0]
    assert argv[-5:] == ["git", "-C", "/home/user/project", "status", "--short"]
    assert result.ok
