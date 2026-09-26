from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field

from relmote.model import Action


@dataclass(frozen=True)
class TransportCapabilities:
    name: str
    bidirectional: bool
    interactive: bool
    works_before_os: bool = False


@dataclass(frozen=True)
class ExecutionContext:
    """Per-dispatch context supplied by the controller.

    `should_stop` is intentionally dynamic: transports must re-check it during
    longer operations so revocation or expiry can stop work already in flight.
    """

    session_id: str
    target_id: str
    should_stop: Callable[[], bool] = field(repr=False, compare=False)


class Transport(ABC):
    """Base interface for Relmote system/controller transport adapters."""

    @property
    @abstractmethod
    def capabilities(self) -> TransportCapabilities:
        raise NotImplementedError

    @abstractmethod
    def execute(self, action: Action, context: ExecutionContext) -> object:
        """Execute an already-authorized action.

        Policy enforcement belongs above this call. Long-running transports
        must observe `context.should_stop()`.
        """
        raise NotImplementedError
