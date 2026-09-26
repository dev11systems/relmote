from relmote.version import build_info


def test_build_info_has_required_fields():
    value = build_info()

    assert value["version"]
    assert "commit" in value
    assert "channel" in value
