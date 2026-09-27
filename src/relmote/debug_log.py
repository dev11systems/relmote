from __future__ import annotations

import logging
import os
from collections import deque
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOGGER_NAME = "relmote"
MAX_LOG_BYTES = 1_000_000
BACKUP_COUNT = 3


def state_directory() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    if base:
        return Path(base) / "relmote"
    return Path.home() / ".local" / "state" / "relmote"


def log_path() -> Path:
    return state_directory() / "relmote.log"


def configure_logging() -> Path:
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    for handler in list(logger.handlers):
        if getattr(handler, "_relmote_file_handler", False):
            current = Path(getattr(handler, "baseFilename", ""))
            if current == path:
                return path
            logger.removeHandler(handler)
            handler.close()

    handler = RotatingFileHandler(
        path,
        maxBytes=MAX_LOG_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    handler._relmote_file_handler = True
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)sZ %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    logger.addHandler(handler)

    try:
        path.chmod(0o600)
    except OSError:
        pass
    return path


def tail_log(lines: int = 100) -> str:
    if lines < 1:
        raise ValueError("lines must be at least 1")
    path = log_path()
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return "".join(deque(handle, maxlen=lines))


def save_log(destination: str | Path, *, lines: int | None = None) -> Path:
    target = Path(destination).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)

    if lines is None:
        source = log_path()
        content = (
            source.read_text(encoding="utf-8", errors="replace")
            if source.exists()
            else ""
        )
    else:
        content = tail_log(lines)

    target.write_text(content, encoding="utf-8")
    try:
        target.chmod(0o600)
    except OSError:
        pass
    return target
