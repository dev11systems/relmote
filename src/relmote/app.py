from __future__ import annotations

import threading
import webbrowser

from .runtime import RelmoteRuntime
from .tui import run_simple_tui
from .webapp import serve_local


def run_app(
    *,
    port: int = 8787,
    open_browser: bool = False,
) -> int:
    runtime = RelmoteRuntime()
    url = f"http://127.0.0.1:{port}"

    web_thread = threading.Thread(
        target=serve_local,
        kwargs={
            "host": "127.0.0.1",
            "port": port,
            "runtime": runtime,
        },
        name="relmote-web",
        daemon=True,
    )
    web_thread.start()

    if open_browser:
        webbrowser.open(url)

    return run_simple_tui(runtime, web_url=url)
