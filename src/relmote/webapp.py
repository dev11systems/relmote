from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .software_node import SoftwareNode


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111111">
<title>Relmote</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}
body{font-family:system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;background:#111;color:#eee}
h1{letter-spacing:.12em;margin-bottom:.2rem}h2{font-size:1rem;text-transform:uppercase;letter-spacing:.08em;color:#bbb}
.card{border:1px solid #555;border-radius:12px;padding:1rem;margin:1rem 0;background:#171717}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem}
button{font:inherit;padding:.65rem .9rem;margin:.2rem;border:1px solid #777;border-radius:8px;background:#222;color:#fff}
button:hover{background:#333}button.danger{border-color:#aaa}
code,pre{background:#222;border-radius:6px}pre{padding:.8rem;overflow:auto;white-space:pre-wrap}
.muted{color:#aaa}.good{font-weight:700}.pill{display:inline-block;border:1px solid #666;border-radius:999px;padding:.2rem .55rem;margin:.15rem;font-size:.85rem}
</style>
</head>
<body>
<h1>RELMOTE</h1>
<div class="muted">Software node · local-only preview</div>

<div class="grid">
 <section class="card"><h2>Node</h2><div id="node">Loading…</div></section>
 <section class="card"><h2>Target</h2><div id="target">Loading…</div></section>
 <section class="card"><h2>Session</h2><div id="session"></div></section>
</div>

<section class="card">
 <h2>Capabilities</h2><div id="caps"></div>
</section>

<section class="card">
 <h2>Read-only diagnostic tasks</h2>
 <button onclick="runTask('system-overview')">System overview</button>
 <button onclick="runTask('network-overview')">Network overview</button>
 <button onclick="runTask('diagnose-network')">Diagnose network</button>
 <button onclick="runTask('storage-overview')">Storage overview</button>
 <p class="muted">Tasks require an active Observe session. S2 exposes no write capabilities.</p>
</section>

<section class="card">
 <h2>Observations</h2>
 <div id="tasks" class="muted">No observations yet.</div>
</section>

<p class="muted">This preview listens only on localhost. Pairing/authentication comes before LAN or remote access.</p>

<script>
async function request(path, method='GET'){
 const r=await fetch(path,{method});
 const data=await r.json();
 if(!r.ok) throw new Error(data.error || r.statusText);
 return data;
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function refresh(){
 const d=await request('/api/v1/snapshot');
 node.innerHTML='<strong>'+esc(d.node.name)+'</strong><br><code>'+esc(d.node.fingerprint)+'</code><br><span class="muted">'+esc(d.node.implementation)+'</span>';
 target.innerHTML='<strong>'+esc(d.target.name)+'</strong><br><span class="muted">'+esc(d.target.relationship)+'</span>';
 caps.innerHTML=d.capabilities.map(x=>'<span class="pill">'+esc(x)+'</span>').join('');
 if(!d.session || d.session.revoked){
   session.innerHTML='<strong>INACTIVE</strong><br><button onclick="startSession()">Start Observe session</button>';
 }else{
   session.innerHTML='<span class="good">OBSERVE</span><br><code>'+esc(d.session.session_id.slice(0,8))+'</code><br><button class="danger" onclick="revoke()">Revoke</button>';
 }
 if(d.tasks.length){
   tasks.innerHTML=d.tasks.slice().reverse().map(t=>{
     const findings=(t.findings||[]).map(f =>
       '<p><strong>['+esc(f.status)+']</strong> '+esc(f.statement)+
       (f.uncertainty?'<br><span class="muted">'+esc(f.uncertainty)+'</span>':'')+'</p>'
     ).join('');
     return '<div class="card"><strong>'+esc(t.task_type)+'</strong><br><span class="muted">'+esc(t.created_at)+'</span>'+
       findings+
       '<details><summary>Raw observations</summary><pre>'+esc(JSON.stringify(t.observations,null,2))+'</pre></details></div>';
   }).join('');
 }else tasks.textContent='No observations yet.';
}
async function startSession(){await request('/api/v1/session','POST');await refresh()}
async function revoke(){await request('/api/v1/session/revoke','POST');await refresh()}
async function runTask(name){
 try{await request('/api/v1/tasks/'+encodeURIComponent(name),'POST');await refresh()}
 catch(e){alert(e.message)}
}
refresh();
</script>
</body></html>
"""


def _json(handler: BaseHTTPRequestHandler, status: HTTPStatus, value: dict) -> None:
    body = json.dumps(value, indent=2, default=str).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(node: SoftwareNode):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/":
                body = INDEX.encode()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
            elif path == "/api/v1/snapshot":
                _json(self, HTTPStatus.OK, node.snapshot())
            elif path == "/api/v1/health":
                _json(self, HTTPStatus.OK, {"status": "ok"})
            else:
                _json(self, HTTPStatus.NOT_FOUND, {"error": "not found"})

        def do_POST(self):
            path = urlparse(self.path).path
            try:
                if path == "/api/v1/session":
                    session = node.start_observe_session()
                    _json(self, HTTPStatus.CREATED, {
                        "session_id": session.session_id,
                        "mode": "observe",
                    })
                elif path == "/api/v1/session/revoke":
                    node.revoke_session()
                    _json(self, HTTPStatus.OK, {"revoked": True})
                elif path.startswith("/api/v1/tasks/"):
                    task_type = path.rsplit("/", 1)[-1]
                    task = node.run_task(task_type)
                    _json(self, HTTPStatus.CREATED, {
                        "task_id": task.task_id,
                        "task_type": task.task_type,
                    })
                else:
                    _json(self, HTTPStatus.NOT_FOUND, {"error": "not found"})
            except PermissionError as exc:
                _json(self, HTTPStatus.FORBIDDEN, {"error": str(exc)})
            except ValueError as exc:
                _json(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})

        def log_message(self, format, *args):
            return

    return Handler


def serve_local(host: str = "127.0.0.1", port: int = 8787) -> None:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError(
            "S1/S2 only permits localhost binding; LAN access requires pairing/authentication"
        )
    node = SoftwareNode()
    server = ThreadingHTTPServer((host, port), make_handler(node))
    print(f"Relmote: http://{host}:{port}")
    print(f"Node fingerprint: {node.identity.fingerprint}")
    print("Local-only read-only software node. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.revoke_session()
        server.server_close()
