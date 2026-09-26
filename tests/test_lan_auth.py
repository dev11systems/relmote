from relmote.lan_auth import TemporaryLANAccess


def test_temporary_lan_token_is_long_and_valid():
    now = [100.0]
    access = TemporaryLANAccess.create(
        lifetime_seconds=60,
        clock=lambda: now[0],
    )

    assert len(access.token) >= 32
    assert access.valid(access.token, clock=lambda: now[0])
    assert not access.valid("wrong", clock=lambda: now[0])


def test_temporary_lan_token_expires():
    now = [100.0]
    access = TemporaryLANAccess.create(
        lifetime_seconds=60,
        clock=lambda: now[0],
    )
    now[0] = 161.0

    assert not access.valid(access.token, clock=lambda: now[0])
