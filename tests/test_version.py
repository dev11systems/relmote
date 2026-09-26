from relmote.version import build_info


def test_build_info_has_required_fields():
    value = build_info()

    assert value["version"]
    assert "commit" in value
    assert "channel" in value


def test_vcs_commit_can_be_read_from_direct_url(monkeypatch):
    import relmote.version as version_module

    class FakeDistribution:
        def read_text(self, name):
            assert name == "direct_url.json"
            return '{"vcs_info":{"vcs":"git","commit_id":"abc123"}}'

    monkeypatch.setattr(version_module, "distribution", lambda name: FakeDistribution())
    assert version_module.installed_vcs_commit() == "abc123"
