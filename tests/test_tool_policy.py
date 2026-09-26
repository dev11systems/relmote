import pytest

from relmote.tool_actions import ToolAction
from relmote.tool_policy import ToolEffect


def test_pytest_is_read_only_in_preview_policy():
    action = ToolAction.create("pytest", ("-q",))
    assert action.effect is ToolEffect.READ_ONLY
    assert not action.requires_approval


def test_mutating_git_action_requires_approval():
    action = ToolAction.create("git", ("add", "README.md"))

    assert action.requires_approval
    with pytest.raises(PermissionError):
        action.mark_executed()

    action.approve()
    action.mark_executed()


def test_unapproved_git_subcommand_is_rejected():
    with pytest.raises(PermissionError):
        ToolAction.create("git", ("commit", "-m", "oops"))


def test_unknown_tool_is_rejected():
    with pytest.raises(PermissionError):
        ToolAction.create("bash", ("-c", "anything"))
