from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .model import Grant


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Session:
    """Mutable authorization state for one controller/target relationship."""

    grant: Grant
    controller_id: str
    session_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=utcnow)
    revoked_at: datetime | None = None
    approved_action_ids: set[str] = field(default_factory=set)
    executed_action_ids: set[str] = field(default_factory=set)

    def is_expired(self, now: datetime | None = None) -> bool:
        if self.grant.expires_at is None:
            return False
        now = now or utcnow()
        return now >= self.grant.expires_at

    def is_active(self, now: datetime | None = None) -> bool:
        return self.revoked_at is None and not self.is_expired(now)

    def revoke(self, now: datetime | None = None) -> None:
        self.revoked_at = now or utcnow()
        self.approved_action_ids.clear()

    def approve(self, action_id: str) -> None:
        self.approved_action_ids.add(action_id)

    def is_approved(self, action_id: str) -> bool:
        return action_id in self.approved_action_ids

    def mark_executed(self, action_id: str) -> None:
        self.executed_action_ids.add(action_id)
        self.approved_action_ids.discard(action_id)

    def was_executed(self, action_id: str) -> bool:
        return action_id in self.executed_action_ids
