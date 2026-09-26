from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class EnvelopeKind(str, Enum):
    TASK = "task"
    APPROVAL = "approval"
    STATUS = "status"
    RESULT = "result"
    EVENT = "event"
    EVIDENCE_REF = "evidence_ref"


@dataclass(frozen=True)
class Envelope:
    """Transport-neutral message suitable for rich or constrained adapters."""

    kind: EnvelopeKind
    payload: dict[str, Any]
    envelope_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str | None = None
    priority: int = 50
    expires_at: str | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.priority <= 100:
            raise ValueError("priority must be between 0 and 100")


@dataclass(frozen=True)
class DeliveryReceipt:
    envelope_id: str
    delivered: bool
    duplicate: bool = False
    detail: str | None = None


class Deduplicator:
    def __init__(self, max_ids: int = 4096) -> None:
        if max_ids <= 0:
            raise ValueError("max_ids must be positive")
        self.max_ids = max_ids
        self._seen: list[str] = []
        self._set: set[str] = set()

    def first_seen(self, envelope_id: str) -> bool:
        if envelope_id in self._set:
            return False

        self._seen.append(envelope_id)
        self._set.add(envelope_id)

        if len(self._seen) > self.max_ids:
            old = self._seen.pop(0)
            self._set.discard(old)

        return True
