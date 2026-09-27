import logging

from relmote.debug_log import configure_logging, log_path, tail_log


def test_debug_log_uses_xdg_state_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))

    path = configure_logging()

    assert path == tmp_path / "relmote" / "relmote.log"
    assert path.parent.is_dir()


def test_debug_log_can_tail_recent_entries(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    path = configure_logging()

    logger = logging.getLogger("relmote.test")
    logger.warning("first debug line")
    logger.error("second debug line")
    for handler in logging.getLogger("relmote").handlers:
        handler.flush()

    content = tail_log(2)

    assert "first debug line" in content
    assert "second debug line" in content
    assert path.exists()
