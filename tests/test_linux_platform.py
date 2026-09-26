from relmote.platforms.linux import _read_os_release


def test_os_release_parser_returns_mapping():
    value = _read_os_release()
    assert isinstance(value, dict)
