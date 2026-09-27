import logging

from relmote.debug_log import configure_logging, log_path, save_log, tail_log


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


def test_save_log_exports_full_active_log(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    configure_logging()
    logger = logging.getLogger("relmote.test")
    logger.warning("export me")
    for handler in logging.getLogger("relmote").handlers:
        handler.flush()

    destination = tmp_path / "relmote-debug.txt"
    written = save_log(destination)

    assert written == destination
    assert "export me" in destination.read_text()


def test_save_log_can_export_only_recent_lines(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    configure_logging()
    logger = logging.getLogger("relmote.test")
    logger.warning("old line")
    logger.warning("new line")
    for handler in logging.getLogger("relmote").handlers:
        handler.flush()

    destination = tmp_path / "recent.txt"
    save_log(destination, lines=1)

    content = destination.read_text()
    assert "new line" in content
    assert "old line" not in content
