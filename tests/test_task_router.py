from relmote.routing import TaskRequirements
from relmote.task_router import TaskRouter
from relmote.tasks import Task, TaskState
from relmote.topology import Feedback, Target, TargetPath


def target_with(*paths):
    return Target("target:1", "Target", tuple(paths))


HID = TargetPath("hid", "usb.hid", Feedback.NONE, works_before_os=True)
SSH = TargetPath(
    "ssh",
    "ssh",
    Feedback.TEXT,
    native=True,
    bidirectional=True,
)


def test_same_task_can_move_to_richer_path():
    task = Task("inspect system", "target:1")
    router = TaskRouter()

    first, first_change = router.choose(
        task,
        target_with(HID),
        TaskRequirements(needs_input=True),
    )
    assert first.path == HID
    assert first_change.new_path_id == "hid"

    second, second_change = router.choose(
        task,
        target_with(HID, SSH),
        TaskRequirements(needs_input=True, needs_text_feedback=True),
    )
    assert second.path == SSH
    assert second_change.previous_path_id == "hid"
    assert second_change.new_path_id == "ssh"
    assert task.task_id == second_change.task_id


def test_path_loss_pauses_running_task():
    task = Task("inspect system", "target:1")
    task.transition(TaskState.PLANNING)
    task.transition(TaskState.READY)
    task.transition(TaskState.RUNNING)

    router = TaskRouter()
    router.choose(task, target_with(HID), TaskRequirements(needs_input=True))
    router.pause_for_path_loss(task)

    assert task.state is TaskState.PAUSED
