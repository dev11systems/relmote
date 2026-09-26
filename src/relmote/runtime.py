from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4

from .software_node import SoftwareNode


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str
    kind: str
    created_at: str
    data: dict


@dataclass
class RelmoteRuntime:
    """Authoritative in-process state shared by all frontends."""

    node: SoftwareNode = field(default_factory=SoftwareNode)
    _events: list[RuntimeEvent] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock)

    def emit(self, kind: str, data: dict | None = None) -> RuntimeEvent:
        event = RuntimeEvent(
            event_id=str(uuid4()),
            kind=kind,
            created_at=utcnow_iso(),
            data=data or {},
        )
        with self._lock:
            self._events.append(event)
            self._events = self._events[-200:]
        return event

    def start_checks(self) -> dict:
        with self._lock:
            session = self.node.start_observe_session()
            self.emit("session.started", {
                "session_id": session.session_id,
                "mode": "observe",
            })
            return self.snapshot()

    def stop_checks(self) -> dict:
        with self._lock:
            self.node.revoke_session()
            self.emit("session.revoked")
            return self.snapshot()

    def run_task(self, task_type: str) -> dict:
        with self._lock:
            task = self.node.run_task(task_type)
            self.emit("task.completed", {
                "task_id": task.task_id,
                "task_type": task.task_type,
            })
            return self.snapshot()

    def events_since(self, offset: int = 0) -> dict:
        with self._lock:
            events = self._events[offset:]
            return {
                "offset": offset + len(events),
                "events": [
                    {
                        "event_id": event.event_id,
                        "kind": event.kind,
                        "created_at": event.created_at,
                        "data": event.data,
                    }
                    for event in events
                ],
            }

    def snapshot(self) -> dict:
        with self._lock:
            value = self.node.snapshot()
            value["runtime"] = {
                "event_count": len(self._events),
                "frontends": ["cli", "tui-preview", "web"],
            }
            return value
