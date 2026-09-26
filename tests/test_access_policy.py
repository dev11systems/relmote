from relmote.access_policy import AccessPolicy, AvailabilityMode


def test_access_is_disabled_by_default():
    assert not AccessPolicy().available()


def test_access_can_remain_enabled_until_manually_disabled():
    policy = AccessPolicy()
    policy.enable_until_disabled()

    assert policy.available()
    assert policy.mode is AvailabilityMode.UNTIL_DISABLED

    policy.disable()
    assert not policy.available()


def test_timed_access_expires_and_returns_to_disabled():
    now = [100.0]
    policy = AccessPolicy()
    policy.enable_for(60, clock=lambda: now[0])

    assert policy.available(clock=lambda: now[0])
    now[0] = 161
    assert not policy.available(clock=lambda: now[0])
    assert policy.mode is AvailabilityMode.DISABLED
