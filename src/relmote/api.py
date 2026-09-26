from __future__ import annotations

from dataclasses import dataclass

from .events import EventStream
from .node_state import NodeState
from .routing import RouteDecision, TaskRequirements, select_system_path


@dataclass
class LocalControllerAPI:
    """Semantic local API facade.

    This is deliberately framework-neutral. A future HTTP/WebSocket, BLE, or
    constrained-link adapter can expose the same operations.
    """

    state: NodeState
    events: EventStream

    def snapshot(self) -> dict:
        return self.state.snapshot()

    def route_task(
        self,
        target_id: str,
        requirements: TaskRequirements,
    ) -> RouteDecision:
        target = self.state.targets.get(target_id)
        if target is None:
            return RouteDecision(
                path=None,
                usable=False,
                reason="unknown target",
            )
        return select_system_path(target.system_paths, requirements)

    def event_snapshot(self, index: int = 0) -> list[dict]:
        return [event.as_dict() for event in self.events.since(index)]
