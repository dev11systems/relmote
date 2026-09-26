from __future__ import annotations

import socket
import threading
import time
import webbrowser

from .runtime import RelmoteRuntime
from .tui import run_simple_tui
from .webapp import serve_local


def wait_for_local_port(
    host: str,
    port: int,
    *,
    timeout: float = 2.0,
) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.15):
                return True
        except OSError:
            time.sleep(0.05)
    return False


def run_app(
    *,
    port: int = 8787,
    open_browser: bool = False,
) -> int:
    runtime = RelmoteRuntime()
    host = "127.0.0.1"
    url = f"http://{host}:{port}"

    web_thread = threading.Thread(
        target=serve_local,
        kwargs={
            "host": host,
            "port": port,
            "runtime": runtime,
        },
        name="relmote-web",
        daemon=True,
    )
    web_thread.start()

    web_ready = wait_for_local_port(host, port)
    runtime.emit(
        "frontend.web.ready" if web_ready else "frontend.web.failed",
        {"url": url},
    )

    if open_browser and web_ready:
        webbrowser.open(url)

    return run_simple_tui(
        runtime,
        web_url=url,
        web_ready=web_ready,
    )
