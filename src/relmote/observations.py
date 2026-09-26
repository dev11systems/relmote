from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class ObservationKind(str, Enum):
    TEXT = "text"
    SCREEN = "screen"
    STRUCTURED = "structured"
    EVENT = "event"


class Completeness(str, Enum):
    COMPLETE = "complete"
    SUMMARIZED = "summarized"
    TRUNCATED = "truncated"


@dataclass(frozen=True)
class Observation:
    target_id: str
    source_transport: str
    kind: ObservationKind
    content: Any
    completeness: Completeness = Completeness.COMPLETE
    observation_id: str = field(default_factory=lambda: str(uuid4()))
    transformed_from: tuple[str, ...] = ()


@dataclass(frozen=True)
class Finding:
    statement: str
    evidence_ids: tuple[str, ...]
    uncertainty: str | None = None


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    findings: tuple[Finding, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    side_effects: tuple[str, ...] = ()
    unresolved: tuple[str, ...] = ()
