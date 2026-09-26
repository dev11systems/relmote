from unittest.mock import patch

from relmote.ssh_workspace import SSHWorkspace
from relmote.workspace import WorkspacePolicy


@patch("relmote.ssh_workspace.subprocess.run")
def test_read_is_confined_and_uses_argv(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "hello"
    mock_run.return_value.stderr = ""

    workspace = SSHWorkspace(
        "cousin-host",
        WorkspacePolicy.create("/home/user/project"),
    )
    result = workspace.read("README.md")

    argv = mock_run.call_args.args[0]
    assert argv[-3:] == ["cat", "--", "/home/user/project/README.md"]
    assert result.stdout == "hello"


@patch("relmote.ssh_workspace.subprocess.run")
def test_git_status_is_explicit_operation(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = " M README.md\n"
    mock_run.return_value.stderr = ""

    workspace = SSHWorkspace(
        "cousin-host",
        WorkspacePolicy.create("/home/user/project"),
    )
    result = workspace.git_status()

    argv = mock_run.call_args.args[0]
    assert argv[-5:] == ["git", "-C", "/home/user/project", "status", "--short"]
    assert result.ok
