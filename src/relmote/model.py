from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class Mode(str, Enum):
    OBSERVE = "observe"
    TEACH = "teach"
    ASSIST = "assist"
    OPERATE = "operate"


@dataclass(frozen=True)
class Action:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    capabilities: tuple[str, ...] = ()
    action_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True)
class Grant:
    capabilities: frozenset[str]
    target_id: str
    mode: Mode
    expires_at: datetime | None = None


@dataclass(frozen=True)
class Decision:
    allowed: bool
    requires_approval: bool
    reason: str


@dataclass(frozen=True)
class ExecutionOutcome:
    executed: bool
    status: str
    reason: str
    result: Any | None = None
