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


def test_build_info_has_short_commit(monkeypatch):
    import relmote.version as version_module

    monkeypatch.setattr(
        version_module,
        "installed_vcs_commit",
        lambda: "1234567890abcdef",
    )
    monkeypatch.delenv("RELMOTE_BUILD_COMMIT", raising=False)
    monkeypatch.delenv("RELMOTE_BUILD_CHANNEL", raising=False)

    value = version_module.build_info()

    assert value["short_commit"] == "12345678"


def test_repository_display_version_is_unique():
    from relmote.version import display_version

    from relmote.dev_revision import DEV_REVISION

    assert (
        display_version(
            "0.1.0.dev0",
            "1234567890abcdef",
            "repository",
        )
        == f"0.1.0-dev.{DEV_REVISION}"
    )


def test_release_display_version_stays_semantic():
    from relmote.version import display_version

    assert display_version("0.1.0", "12345678", "stable") == "0.1.0"
