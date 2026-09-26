import pytest

from relmote.webapp import serve_local


def test_non_loopback_requires_explicit_lan_mode():
    with pytest.raises(ValueError, match="explicit --lan"):
        serve_local(host="0.0.0.0", port=0)
