from __future__ import annotations

import socket
import secrets
import threading
import time
import webbrowser

from .network_exposure import ExposureChoice, choose_exposure
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
    exposure_mode: str = "auto",
    bind_host: str | None = None,
) -> int:
    runtime = RelmoteRuntime()
    exposure = choose_exposure(
        "custom" if bind_host else exposure_mode,
        custom_host=bind_host,
    )
    host = exposure.bind_host
    remote_token = (
        secrets.token_urlsafe(24)
        if exposure.mode.value != "localhost"
        else None
    )
    url = f"http://{host}:{port}"
    display_url = (
        f"{url}/?token={remote_token}"
        if remote_token
        else url
    )

    web_thread = threading.Thread(
        target=serve_local,
        kwargs={
            "host": host,
            "port": port,
            "runtime": runtime,
            "explicit_private_bind": exposure.private,
            "explicit_lan_bind": exposure.mode.value == "lan",
            "access_token": remote_token,
        },
        name="relmote-web",
        daemon=True,
    )
    web_thread.start()

    web_ready = wait_for_local_port(host, port)
    runtime.emit(
        "frontend.web.ready" if web_ready else "frontend.web.failed",
        {
            "url": display_url,
            "exposure_mode": exposure.mode.value,
            "description": exposure.description,
        },
    )

    if open_browser and web_ready:
        webbrowser.open(display_url)

    return run_simple_tui(
        runtime,
        web_url=display_url,
        web_ready=web_ready,
        web_exposure=exposure.description,
    )
