from __future__ import annotations

from dataclasses import dataclass, field

from .ssh_workspace import SSHWorkspace
from .workspace_changes import FileChangeProposal, digest_text


@dataclass
class WorkspaceService:
    workspace: SSHWorkspace
    proposals: dict[str, FileChangeProposal] = field(default_factory=dict)

    def propose_write(self, path: str, new_content: str) -> FileChangeProposal:
        current = self.workspace.read(path)
        if not current.ok:
            raise RuntimeError(current.stderr or "unable to read current file")
        proposal = FileChangeProposal(
            path=path,
            before=current.stdout,
            after=new_content,
        )
        self.proposals[proposal.proposal_id] = proposal
        return proposal

    def approve(self, proposal_id: str) -> FileChangeProposal:
        proposal = self._proposal(proposal_id)
        proposal.approve()
        return proposal

    def reject(self, proposal_id: str) -> FileChangeProposal:
        proposal = self._proposal(proposal_id)
        proposal.reject()
        return proposal

    def apply(self, proposal_id: str):
        proposal = self._proposal(proposal_id)
        if proposal.state.value != "approved":
            raise PermissionError("proposal is not approved")

        # Optimistic concurrency guard: refuse to overwrite if the remote file
        # changed after the proposal was created.
        current = self.workspace.read(proposal.path)
        if not current.ok:
            raise RuntimeError(current.stderr or "unable to re-read current file")
        if digest_text(current.stdout) != proposal.before_sha256:
            raise RuntimeError(
                "remote file changed since proposal; refresh and propose again"
            )

        result = self.workspace.write_text(proposal.path, proposal.after)
        if not result.ok:
            raise RuntimeError(result.stderr or "remote write failed")

        verify = self.workspace.read(proposal.path)
        if not verify.ok:
            raise RuntimeError(verify.stderr or "unable to verify remote write")
        if digest_text(verify.stdout) != proposal.after_sha256:
            raise RuntimeError("remote write verification digest mismatch")

        proposal.mark_applied()
        return result

    def _proposal(self, proposal_id: str) -> FileChangeProposal:
        try:
            return self.proposals[proposal_id]
        except KeyError as exc:
            raise KeyError(f"unknown proposal: {proposal_id}") from exc
