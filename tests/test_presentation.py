from relmote.presentation import (
    availability_label,
    capability_label,
    effect_label,
)


def test_internal_capabilities_have_plain_language_labels():
    assert capability_label("network.inspect") == "View network information"
    assert capability_label("file.write") == "Edit files"


def test_access_state_is_human_readable():
    assert availability_label("disabled") == "Support off"
    assert availability_label("until-disabled") == "Support on until you turn it off"


def test_tool_effect_does_not_claim_tests_are_read_only():
    assert effect_label("workspace-execution") == "Run a project tool"
