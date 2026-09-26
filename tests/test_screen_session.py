from relmote.screen_session import ScreenSession, ScreenState


def test_screen_observe_requires_relmote_then_os_consent():
    session = ScreenSession()

    assert session.state is ScreenState.REQUESTED
    session.approve()
    assert session.state is ScreenState.APPROVED
    session.awaiting_os_consent()
    assert session.state is ScreenState.OS_CONSENT
    session.activate()
    assert session.state is ScreenState.ACTIVE


def test_screen_failure_is_visible():
    session = ScreenSession()
    session.fail("portal unavailable")

    assert session.state is ScreenState.FAILED
    assert session.error == "portal unavailable"
