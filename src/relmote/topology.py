from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Reachability(str, Enum):
    INTERACTIVE = "online-interactive"
    CONSTRAINED = "online-constrained"
    STORE_FORWARD = "store-and-forward"
    OFFLINE = "offline"


class Feedback(str, Enum):
    NONE = "none"
    TEXT = "text"
    SCREEN = "screen"
    STRUCTURED = "structured"


@dataclass(frozen=True)
class Path:
    path_id: str
    transport: str
    interactive: bool
    constrained: bool = False
    encrypted: bool = False
    authenticated: bool = False
    bandwidth_bps: int | None = None
    latency_ms: int | None = None


@dataclass(frozen=True)
class TargetPath:
    path_id: str
    transport: str
    feedback: Feedback
    works_before_os: bool = False
    native: bool = False
    bidirectional: bool = False


@dataclass(frozen=True)
class Node:
    node_id: str
    name: str
    controller_paths: tuple[Path, ...]


@dataclass(frozen=True)
class Target:
    target_id: str
    name: str
    system_paths: tuple[TargetPath, ...]


def reachability(paths: tuple[Path, ...]) -> Reachability:
    if any(path.interactive and not path.constrained for path in paths):
        return Reachability.INTERACTIVE
    if any(path.interactive and path.constrained for path in paths):
        return Reachability.CONSTRAINED
    if paths:
        return Reachability.STORE_FORWARD
    return Reachability.OFFLINE
