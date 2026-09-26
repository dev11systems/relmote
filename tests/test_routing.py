from relmote.routing import TaskRequirements, select_system_path
from relmote.topology import Feedback, TargetPath


HID = TargetPath(
    path_id="hid",
    transport="usb.hid",
    feedback=Feedback.NONE,
    works_before_os=True,
    native=False,
    bidirectional=False,
)

SSH = TargetPath(
    path_id="ssh",
    transport="ssh",
    feedback=Feedback.TEXT,
    works_before_os=False,
    native=True,
    bidirectional=True,
)

KVM = TargetPath(
    path_id="kvm",
    transport="kvm",
    feedback=Feedback.SCREEN,
    works_before_os=True,
    native=False,
    bidirectional=True,
)


def test_prefers_native_ssh_for_text_task():
    result = select_system_path(
        (HID, SSH, KVM),
        TaskRequirements(needs_input=True, needs_text_feedback=True),
    )

    assert result.usable
    assert result.path == SSH


def test_preboot_screen_task_selects_kvm():
    result = select_system_path(
        (HID, SSH, KVM),
        TaskRequirements(
            needs_input=True,
            needs_screen_feedback=True,
            needs_preboot=True,
        ),
    )

    assert result.path == KVM


def test_blind_hid_surfaces_limitation():
    result = select_system_path(
        (HID,),
        TaskRequirements(needs_input=True),
    )

    assert result.path == HID
    assert "no target feedback" in result.limitations


def test_hid_cannot_satisfy_text_feedback_requirement():
    result = select_system_path(
        (HID,),
        TaskRequirements(needs_input=True, needs_text_feedback=True),
    )

    assert not result.usable
    assert result.path is None
