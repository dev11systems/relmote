import pytest

from relmote.tasks import Task, TaskState


def test_valid_task_lifecycle():
    task = Task("inspect network", "target:router")
    task.transition(TaskState.PLANNING)
    task.transition(TaskState.WAITING_APPROVAL)
    task.transition(TaskState.READY)
    task.transition(TaskState.RUNNING)
    task.transition(TaskState.WAITING_OBSERVATION)
    task.transition(TaskState.RUNNING)
    task.transition(TaskState.COMPLETED)

    assert task.terminal


def test_invalid_transition_fails():
    task = Task("inspect network", "target:router")

    with pytest.raises(ValueError, match="invalid task transition"):
        task.transition(TaskState.RUNNING)


def test_terminal_task_cannot_restart():
    task = Task("inspect network", "target:router")
    task.transition(TaskState.CANCELLED)

    with pytest.raises(ValueError, match="terminal"):
        task.transition(TaskState.PLANNING)
