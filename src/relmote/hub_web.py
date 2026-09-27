from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .hub_inventory import HubInventory
from .lan_auth import TemporaryLANAccess
from .network_exposure import choose_exposure


HUB_INDEX = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111111">
<title>Relmote Hub</title>
<style>
:root{color-scheme:dark}
*{box-sizing:border-box}
body{font-family:system-ui,sans-serif;max-width:980px;margin:1.5rem auto;padding:0 1rem;background:#111;color:#eee}
h1{letter-spacing:.1em;margin:.1rem 0}
h2{font-size:.95rem;text-transform:uppercase;letter-spacing:.08em;color:#bbb}
.card{border:1px solid #555;border-radius:12px;padding:1rem;margin:1rem 0;background:#171717}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.8rem}
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.6rem}
.metric{border:1px solid #444;border-radius:10px;padding:.8rem;background:#151515}
.metric strong{display:block;font-size:1.45rem}
.muted{color:#aaa}
.pill{display:inline-block;border:1px solid #666;border-radius:999px;padding:.2rem .55rem;margin:.12rem;font-size:.82rem}
.target{border-left:4px solid #666}
.target.active{border-left-color:#7a7}
.target.revoked,.target.stale_credential,.target.denied{border-left-color:#aa8}
.target.unreachable{border-left-color:#a77}
code{background:#222;border-radius:5px;padding:.08rem .28rem}
button{font:inherit;padding:.6rem .85rem;border:1px solid #777;border-radius:8px;background:#222;color:#fff}
button:hover{background:#333}
.row{display:flex;gap:.6rem;align-items:center;justify-content:space-between;flex-wrap:wrap}
.small{font-size:.9rem}
@media(max-width:600px){body{margin:.7rem auto}.grid{grid-template-columns:1fr}.card{padding:.85rem}}
</style>
</head>
<body>
<div class="row">
  <div>
    <h1>RELMOTE HUB</h1>
    <div class="muted">Read-only local inventory</div>
  </div>
  <button onclick="refreshHub()">Refresh</button>
</div>
<div id="error" class="card" style="display:none;border-color:#a77"></div>
<section class="card">
  <h2>Summary</h2>
  <div id="summary" class="summary"><div class="muted">Loading…</div></div>
</section>
<section class="card">
  <h2>Agent Host</h2>
  <div id="host" class="muted">Loading…</div>
</section>
<section>
  <h2>Paired Targets</h2>
  <div id="targets"><div class="card muted">Loading…</div></div>
</section>
<p class="muted small">
This Hub preview is inventory-only. It cannot create Target grants, execute Target operations, update nodes, or relay traffic.
</p>
<script>
const token=new URLSearchParams(location.search).get('token');
function esc(value){
  return String(value??'')
    .replaceAll('&','&amp;').replaceAll('<','&lt;')
    .replaceAll('>','&gt;').replaceAll('"','&quot;');
}
function pills(values){
  const items=values||[];
  return items.length ? items.map(v=>'<span class="pill">'+esc(v)+'</span>').join('') : '<span class="muted">none</span>';
}
function metric(label,value){
  return '<div class="metric"><strong>'+esc(value)+'</strong><span class="muted">'+esc(label)+'</span></div>';
}
function targetCard(item){
  const current=item.current||{};
  const live=item.live||{};
  const health=current.health||'not-probed';
  const cls='card target '+health;
  let html='<div class="'+cls+'">';
  html+='<div class="row"><strong>'+esc(item.name)+'</strong><span class="pill">'+esc(health)+'</span></div>';
  html+='<p><span class="muted">Workspace:</span> <code>'+esc(item.workspace||'?')+'</code></p>';
  html+='<p><span class="muted">Paired profile state (cached):</span> '+esc(item.state||'?')+'</p>';
  html+='<div><span class="muted">Paired profile capabilities (cached):</span><br>'+pills(item.capabilities)+'</div>';
  if(item.live){
    const reach=live.reachable===true?'reachable':(live.reachable===false?'unreachable':'unknown');
    html+='<p><span class="muted">Live:</span> '+esc(reach)+' · '+esc(live.authority||'unknown')+'</p>';
    if(live.state) html+='<p><span class="muted">Live state:</span> '+esc(live.state)+'</p>';
    if(live.detail) html+='<p><span class="muted">Detail:</span> '+esc(live.detail)+'</p>';
  }
  if(current.recommended_action){
    html+='<p><strong>Attention:</strong> '+esc(current.recommended_action)+'</p>';
  }
  html+='</div>';
  return html;
}
async function refreshHub(){
  const err=document.getElementById('error');
  err.style.display='none';
  const q=token?'?token='+encodeURIComponent(token):'';
  try{
    const r=await fetch('/api/inventory'+q,{cache:'no-store'});
    const value=await r.json();
    if(!r.ok) throw new Error(value.error||('HTTP '+r.status));
    const s=value.summary||{};
    document.getElementById('summary').innerHTML=
      metric('paired targets',s.total||0)+
      metric('active',s.active||0)+
      metric('need attention',s.attention||0)+
      metric('revoked',s.revoked||0)+
      metric('stale credentials',s.stale_credential||0)+
      metric('unreachable',s.unreachable||0);
    const h=value.agent_host||{};
    const b=h.relmote||{};
    document.getElementById('host').innerHTML=
      '<div class="grid">'+
      '<div><strong>'+esc(h.name||'?')+'</strong><br><span class="muted">'+esc(h.platform||'?')+' / '+esc(h.architecture||'?')+'</span></div>'+
      '<div><strong>'+esc(b.display_version||'?')+'</strong><br><span class="muted">build '+esc(b.short_commit||'?')+'</span></div>'+
      '</div>'+
      '<p><span class="muted">Capabilities:</span><br>'+pills(h.capabilities)+'</p>'+
      '<p><span class="muted">Tools:</span><br>'+pills(h.tools)+'</p>';
    const targets=value.paired_targets||[];
    document.getElementById('targets').innerHTML=
      targets.length ? targets.map(targetCard).join('') : '<div class="card muted">No paired Relmote Targets.</div>';
  }catch(e){
    err.textContent='Hub refresh failed: '+e.message;
    err.style.display='block';
  }
}
refreshHub();
setInterval(refreshHub,15000);
</script>
</body>
</html>
"""


def _json(handler: BaseHTTPRequestHandler, status: HTTPStatus, value: dict) -> None:
    body = json.dumps(value, indent=2, default=str).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def _authorized(access, path: str) -> bool:
    if access is None:
        return True
    query = parse_qs(urlparse(path).query)
    candidate = (query.get("token") or [None])[0]
    return access.valid(candidate)


def make_hub_handler(
    inventory: HubInventory,
    access=None,
):
    class HubHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if not _authorized(access, self.path):
                _json(self, HTTPStatus.FORBIDDEN, {"error": "invalid or expired Hub token"})
                return

            if parsed.path == "/":
                body = HUB_INDEX.encode()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
                return

            if parsed.path == "/api/inventory":
                _json(self, HTTPStatus.OK, inventory.snapshot(live=True))
                return

            _json(self, HTTPStatus.NOT_FOUND, {"error": "not found"})

        def do_POST(self):
            _json(self, HTTPStatus.METHOD_NOT_ALLOWED, {
                "error": "Hub preview is read-only",
            })

        def log_message(self, format, *args):
            return

    return HubHandler


def serve_hub(
    *,
    port: int = 8790,
    tailscale: bool = False,
    lifetime_minutes: int = 60,
    inventory: HubInventory | None = None,
) -> None:
    if tailscale:
        exposure = choose_exposure("tailscale")
        access = TemporaryLANAccess.create(
            lifetime_seconds=lifetime_minutes * 60
        )
    else:
        exposure = choose_exposure("localhost")
        access = None

    inventory = inventory or HubInventory()
    server = ThreadingHTTPServer(
        (exposure.bind_host, port),
        make_hub_handler(inventory, access),
    )

    if access:
        print("RELMOTE HUB — private read-only preview")
        print(
            f"http://{exposure.bind_host}:{port}/?token={access.token}"
        )
        print(f"expires in {lifetime_minutes} minutes")
        print("Bound only to the detected Tailscale IPv4 address.")
    else:
        print("RELMOTE HUB — local read-only preview")
        print(f"http://{exposure.bind_host}:{port}/")
        print("Bound to localhost only.")

    print("Inventory refreshes every 15 seconds. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
