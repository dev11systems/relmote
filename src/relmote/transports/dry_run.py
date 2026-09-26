from __future__ import annotations

from relmote.model import Action

from .base import Transport, TransportCapabilities


class DryRunTransport(Transport):
    """Transport used for development before hardware output exists."""

    @property
    def capabilities(self) -> TransportCapabilities:
        return TransportCapabilities(
            name="dry-run",
            bidirectional=True,
            interactive=False,
            works_before_os=False,
        )

    def execute(self, action: Action) -> object:
        return {
            "transport": "dry-run",
            "executed": False,
            "action": {
                "kind": action.kind,
                "payload": action.payload,
                "capabilities": list(action.capabilities),
            },
        }
