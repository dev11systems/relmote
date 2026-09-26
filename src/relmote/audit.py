from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    session_id: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utcnow_iso)
    action_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class AuditLog:
    """Append-only in-memory audit log.

    Payload contents are intentionally not logged by the controller by default;
    commands, typed text, and other sensitive material should require an
    explicit future logging policy.
    """

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        event_type: str,
        session_id: str,
        *,
        action_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_type=event_type,
            session_id=session_id,
            action_id=action_id,
            details=details or {},
        )
        self._events.append(event)
        return event

    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(event.as_dict(), sort_keys=True) for event in self._events)
