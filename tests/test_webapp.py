import pytest

from relmote.webapp import serve_local


def test_non_loopback_requires_explicit_lan_mode():
    with pytest.raises(ValueError, match="explicit private or LAN"):
        serve_local(host="0.0.0.0", port=0)


def test_arbitrary_non_loopback_still_requires_explicit_exposure():
    with pytest.raises(ValueError, match="explicit private or LAN"):
        serve_local(host="192.0.2.10", port=0)
