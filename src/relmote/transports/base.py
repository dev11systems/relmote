from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from relmote.model import Action


@dataclass(frozen=True)
class TransportCapabilities:
    name: str
    bidirectional: bool
    interactive: bool
    works_before_os: bool = False


class Transport(ABC):
    """Base interface for Relmote system/controller transport adapters."""

    @property
    @abstractmethod
    def capabilities(self) -> TransportCapabilities:
        raise NotImplementedError

    @abstractmethod
    def execute(self, action: Action) -> object:
        """Execute an already-authorized action.

        Policy enforcement belongs above this call.
        """
        raise NotImplementedError
