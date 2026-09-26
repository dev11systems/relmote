from relmote.feature_status import remote_feature_status


def test_feature_status_does_not_advertise_unimplemented_screen():
    value = remote_feature_status()

    assert value["screen"]["available"] is False
    assert value["screen"]["control_available"] is False
    assert "terminal" in value
