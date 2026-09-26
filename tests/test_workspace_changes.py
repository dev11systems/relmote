import pytest

from relmote.workspace_changes import ChangeState, FileChangeProposal


def test_proposal_has_diff_and_hashes():
    p = FileChangeProposal("README.md", "old\n", "new\n")

    assert "-old" in p.diff()
    assert "+new" in p.diff()
    assert p.before_sha256 != p.after_sha256


def test_apply_state_requires_approval():
    p = FileChangeProposal("README.md", "old", "new")

    with pytest.raises(ValueError):
        p.mark_applied()

    p.approve()
    p.mark_applied()
    assert p.state is ChangeState.APPLIED
