from relmote.screen_backend import detect_linux_screen_backend


def test_screen_backend_detection_is_honest_about_implementation():
    status = detect_linux_screen_backend()

    assert status.observe_implemented is False
    assert status.control_implemented is False
    assert status.session_type
