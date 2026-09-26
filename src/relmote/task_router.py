from __future__ import annotations

from dataclasses import dataclass

from .routing import RouteDecision, TaskRequirements, select_system_path
from .tasks import Task, TaskState
from .topology import Target


@dataclass(frozen=True)
class RouteChange:
    task_id: str
    previous_path_id: str | None
    new_path_id: str | None
    reason: str


class TaskRouter:
    """Tracks technical route selection separately from task identity."""

    def __init__(self) -> None:
        self._active_path: dict[str, str] = {}

    def choose(
        self,
        task: Task,
        target: Target,
        requirements: TaskRequirements,
    ) -> tuple[RouteDecision, RouteChange | None]:
        decision = select_system_path(target.system_paths, requirements)
        previous = self._active_path.get(task.task_id)
        new = decision.path.path_id if decision.path else None

        change = None
        if previous != new:
            change = RouteChange(
                task_id=task.task_id,
                previous_path_id=previous,
                new_path_id=new,
                reason=decision.reason,
            )

        if decision.usable and new is not None:
            self._active_path[task.task_id] = new
        else:
            self._active_path.pop(task.task_id, None)

        return decision, change

    def pause_for_path_loss(self, task: Task) -> None:
        if task.state in {
            TaskState.RUNNING,
            TaskState.WAITING_OBSERVATION,
        }:
            task.transition(TaskState.PAUSED)
        self._active_path.pop(task.task_id, None)
