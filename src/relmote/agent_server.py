from __future__ import annotations

import json
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread, current_thread

from .agent_api import handle_get, handle_post
from .network_exposure import tailscale_ipv4
from .runtime import RelmoteRuntime


def _json(handler, status: HTTPStatus, value: dict) -> None:
    body = json.dumps(value, indent=2, default=str).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def make_agent_handler(runtime: RelmoteRuntime):
    class AgentHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                value = handle_get(runtime, self.headers, self.path)
            except PermissionError as exc:
                _json(self, HTTPStatus.FORBIDDEN, {"error": str(exc)})
            except KeyError as exc:
                _json(self, HTTPStatus.NOT_FOUND, {"error": str(exc)})
            else:
                _json(self, HTTPStatus.OK, value)

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length) or b"{}")
                value = handle_post(runtime, self.headers, self.path, payload)
            except PermissionError as exc:
                _json(self, HTTPStatus.FORBIDDEN, {"error": str(exc)})
            except (ValueError, KeyError, OSError) as exc:
                _json(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            else:
                _json(self, HTTPStatus.OK, value)

        def log_message(self, format, *args):
            return

    return AgentHandler


@dataclass
class AgentAPIListener:
    host: str
    port: int
    server: ThreadingHTTPServer
    thread: Thread

    @property
    def running(self) -> bool:
        return self.thread.is_alive()

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        if self.thread is not current_thread() and self.thread.is_alive():
            self.thread.join(timeout=2)


def start_tailscale_agent_api(
    runtime: RelmoteRuntime,
    port: int = 8788,
) -> AgentAPIListener:
    host = tailscale_ipv4()
    if not host:
        raise RuntimeError("Tailscale is not connected or has no IPv4 address")

    server = ThreadingHTTPServer((host, port), make_agent_handler(runtime))
    thread = Thread(
        target=server.serve_forever,
        daemon=True,
        name="relmote-agent-tailscale",
    )
    thread.start()
    return AgentAPIListener(
        host=host,
        port=port,
        server=server,
        thread=thread,
    )


def serve_agent_api(
    runtime: RelmoteRuntime,
    host: str = "127.0.0.1",
    port: int = 8788,
) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError(
            "agent API preview binds directly only through the dedicated "
            "Tailscale listener; arbitrary non-loopback binds are rejected"
        )
    server = ThreadingHTTPServer((host, port), make_agent_handler(runtime))
    try:
        server.serve_forever()
    finally:
        server.server_close()
