from __future__ import annotations

from relmote.model import Action

from .base import Transport, TransportCapabilities


class DryRunTransport(Transport):
    """Development transport with no target-side effects."""

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
            "simulated": True,
            "would_execute": True,
            "action": {
                "action_id": action.action_id,
                "kind": action.kind,
                "payload": action.payload,
                "capabilities": list(action.capabilities),
            },
        }
