from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .agent import LocalAgent


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relmote</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:3rem auto;padding:0 1rem;background:#111;color:#eee}
h1{letter-spacing:.08em} .card{border:1px solid #555;border-radius:12px;padding:1rem;margin:1rem 0}
code,pre{background:#222;padding:.2rem .35rem;border-radius:4px} button{font:inherit;padding:.6rem 1rem}
small{color:#aaa}
</style>
</head>
<body>
<h1>RELMOTE</h1>
<p><strong>Software node · local-only S1</strong></p>
<div class="card">
  <div id="identity">Loading node…</div>
</div>
<div class="card">
  <h2>Read-only observations</h2>
  <button onclick="refresh()">Refresh</button>
  <pre id="observations"></pre>
</div>
<p><small>This S1 server binds to localhost only. Remote/LAN access waits for pairing and authentication.</small></p>
<script>
async function refresh(){
 const r=await fetch('/api/v1/snapshot');
 const d=await r.json();
 document.getElementById('identity').textContent =
   d.observations['system.identify'].hostname + ' · ' +
   d.observations['system.platform'].system;
 document.getElementById('observations').textContent =
   JSON.stringify(d,null,2);
}
refresh();
</script>
</body>
</html>
"""


def make_handler(agent: LocalAgent):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/":
                body = INDEX.encode()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            elif path == "/api/v1/snapshot":
                body = json.dumps(agent.snapshot(), indent=2).encode()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
            elif path == "/api/v1/health":
                body = b'{"status":"ok"}'
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
            else:
                body = b'{"error":"not found"}'
                self.send_response(HTTPStatus.NOT_FOUND)
                self.send_header("Content-Type", "application/json")

            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            return

    return Handler


def serve_local(host: str = "127.0.0.1", port: int = 8787) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError(
            "S1 only permits localhost binding; LAN access requires pairing/authentication"
        )

    agent = LocalAgent()
    server = ThreadingHTTPServer((host, port), make_handler(agent))
    print(f"Relmote S1: http://{host}:{port}")
    print("Local-only read-only Agent. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
