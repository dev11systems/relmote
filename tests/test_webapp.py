import pytest

from relmote.webapp import serve_local


def test_s1_refuses_non_loopback_binding():
    with pytest.raises(ValueError, match="localhost"):
        serve_local(host="0.0.0.0", port=0)
