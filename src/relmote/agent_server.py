from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .agent_api import handle_get, handle_post
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


def serve_agent_api(
    runtime: RelmoteRuntime,
    host: str = "127.0.0.1",
    port: int = 8788,
) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError(
            "agent API preview binds only to loopback; use an explicitly "
            "authorized private-network forward/tunnel for remote access"
        )
    server = ThreadingHTTPServer((host, port), make_agent_handler(runtime))
    try:
        server.serve_forever()
    finally:
        server.server_close()
