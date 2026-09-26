from __future__ import annotations

import difflib
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class ChangeState(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    APPLIED = "applied"
    REJECTED = "rejected"


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


@dataclass
class FileChangeProposal:
    path: str
    before: str
    after: str
    proposal_id: str = field(default_factory=lambda: str(uuid4()))
    state: ChangeState = ChangeState.PROPOSED

    @property
    def before_sha256(self) -> str:
        return digest_text(self.before)

    @property
    def after_sha256(self) -> str:
        return digest_text(self.after)

    def diff(self) -> str:
        return "".join(
            difflib.unified_diff(
                self.before.splitlines(keepends=True),
                self.after.splitlines(keepends=True),
                fromfile=f"a/{self.path}",
                tofile=f"b/{self.path}",
            )
        )

    def approve(self) -> None:
        if self.state is not ChangeState.PROPOSED:
            raise ValueError("only proposed changes can be approved")
        self.state = ChangeState.APPROVED

    def reject(self) -> None:
        if self.state is not ChangeState.PROPOSED:
            raise ValueError("only proposed changes can be rejected")
        self.state = ChangeState.REJECTED

    def mark_applied(self) -> None:
        if self.state is not ChangeState.APPROVED:
            raise ValueError("change must be approved before apply")
        self.state = ChangeState.APPLIED
