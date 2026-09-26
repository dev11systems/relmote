from __future__ import annotations

from relmote.model import Action

from .base import ExecutionContext, Transport, TransportCapabilities


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

    def execute(self, action: Action, context: ExecutionContext) -> object:
        return {
            "transport": "dry-run",
            "simulated": True,
            "would_execute": not context.should_stop(),
            "session_id": context.session_id,
            "target_id": context.target_id,
            "action": {
                "action_id": action.action_id,
                "kind": action.kind,
                "payload": action.payload,
                "capabilities": list(action.capabilities),
            },
        }
