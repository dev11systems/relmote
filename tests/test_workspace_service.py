from dataclasses import dataclass

import pytest

from relmote.workspace_changes import ChangeState
from relmote.workspace_service import WorkspaceService


@dataclass
class Result:
    stdout: str = ""
    stderr: str = ""
    ok: bool = True


class FakeWorkspace:
    def __init__(self, value="old\n"):
        self.value = value
        self.writes = []

    def read(self, path):
        return Result(stdout=self.value)

    def write_text(self, path, content):
        self.writes.append((path, content))
        self.value = content
        return Result()


def test_write_requires_explicit_approval():
    ws = FakeWorkspace()
    service = WorkspaceService(ws)
    proposal = service.propose_write("README.md", "new\n")

    with pytest.raises(PermissionError):
        service.apply(proposal.proposal_id)

    assert ws.writes == []


def test_approved_write_is_applied_and_verified():
    ws = FakeWorkspace()
    service = WorkspaceService(ws)
    proposal = service.propose_write("README.md", "new\n")
    service.approve(proposal.proposal_id)

    service.apply(proposal.proposal_id)

    assert proposal.state is ChangeState.APPLIED
    assert ws.value == "new\n"


def test_changed_remote_file_blocks_stale_proposal():
    ws = FakeWorkspace()
    service = WorkspaceService(ws)
    proposal = service.propose_write("README.md", "new\n")
    service.approve(proposal.proposal_id)
    ws.value = "someone else edited this\n"

    with pytest.raises(RuntimeError, match="changed since proposal"):
        service.apply(proposal.proposal_id)

    assert ws.writes == []
