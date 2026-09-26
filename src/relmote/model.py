from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


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


@dataclass(frozen=True)
class Grant:
    capabilities: frozenset[str]
    target_id: str
    mode: Mode


@dataclass(frozen=True)
class Decision:
    allowed: bool
    requires_approval: bool
    reason: str
