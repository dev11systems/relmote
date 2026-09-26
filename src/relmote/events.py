from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Event:
    event_type: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utcnow_iso)
    node_id: str | None = None
    target_id: str | None = None
    session_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventStream:
    """In-memory event stream used before persistent daemon storage exists."""

    def __init__(self, max_events: int = 1000) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be positive")
        self.max_events = max_events
        self._events: list[Event] = []

    def publish(self, event: Event) -> None:
        self._events.append(event)
        overflow = len(self._events) - self.max_events
        if overflow > 0:
            del self._events[:overflow]

    def since(self, index: int = 0) -> tuple[Event, ...]:
        if index < 0:
            raise ValueError("index must be non-negative")
        return tuple(self._events[index:])
