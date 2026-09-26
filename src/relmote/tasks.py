from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class TaskState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    WAITING_APPROVAL = "waiting_approval"
    WAITING_CAPABILITY = "waiting_capability"
    READY = "ready"
    RUNNING = "running"
    WAITING_OBSERVATION = "waiting_observation"
    PAUSED = "paused"
    REJECTED = "rejected"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


_TERMINAL = frozenset(
    {
        TaskState.REJECTED,
        TaskState.FAILED,
        TaskState.COMPLETED,
        TaskState.CANCELLED,
    }
)


_ALLOWED: dict[TaskState, frozenset[TaskState]] = {
    TaskState.CREATED: frozenset(
        {TaskState.PLANNING, TaskState.CANCELLED}
    ),
    TaskState.PLANNING: frozenset(
        {
            TaskState.WAITING_APPROVAL,
            TaskState.WAITING_CAPABILITY,
            TaskState.READY,
            TaskState.FAILED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.WAITING_APPROVAL: frozenset(
        {
            TaskState.READY,
            TaskState.REJECTED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.WAITING_CAPABILITY: frozenset(
        {
            TaskState.PLANNING,
            TaskState.READY,
            TaskState.FAILED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.READY: frozenset(
        {TaskState.RUNNING, TaskState.CANCELLED}
    ),
    TaskState.RUNNING: frozenset(
        {
            TaskState.WAITING_OBSERVATION,
            TaskState.PAUSED,
            TaskState.FAILED,
            TaskState.COMPLETED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.WAITING_OBSERVATION: frozenset(
        {
            TaskState.RUNNING,
            TaskState.PAUSED,
            TaskState.FAILED,
            TaskState.COMPLETED,
            TaskState.CANCELLED,
        }
    ),
    TaskState.PAUSED: frozenset(
        {
            TaskState.PLANNING,
            TaskState.READY,
            TaskState.FAILED,
            TaskState.CANCELLED,
        }
    ),
}


@dataclass(frozen=True)
class TaskConstraints:
    read_only: bool = False
    autonomous_continuation: bool = False
    expires_at: datetime | None = None
    max_actions: int | None = None


@dataclass
class Task:
    intent: str
    target_id: str
    constraints: TaskConstraints = field(default_factory=TaskConstraints)
    task_id: str = field(default_factory=lambda: str(uuid4()))
    state: TaskState = TaskState.CREATED
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def terminal(self) -> bool:
        return self.state in _TERMINAL

    def transition(self, new_state: TaskState) -> None:
        if self.terminal:
            raise ValueError(f"task is terminal: {self.state.value}")

        allowed = _ALLOWED.get(self.state, frozenset())
        if new_state not in allowed:
            raise ValueError(
                f"invalid task transition: {self.state.value} -> {new_state.value}"
            )

        self.state = new_state
