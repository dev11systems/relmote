from __future__ import annotations

import json
import base64
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .software_node import SoftwareNode
from .runtime import RelmoteRuntime
from .report import export_support_report
from .lan_auth import TemporaryLANAccess
from .presentation import capability_label
from .help import render_help
from .project_info import PROJECT_URL, ISSUES_URL, CHANGELOG_URL, bundled_changelog
from .version import build_info
from .agent_controller_api import handle as agent_controller_handle
import tempfile
import socket
import secrets


INDEX = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#111111">
<title>Relmote</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}
body{font-family:system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;background:#111;color:#eee}
h1{letter-spacing:.12em;margin:0}.brand-row{display:flex;align-items:baseline;gap:.65rem;flex-wrap:wrap;margin-bottom:.2rem}.brand-version{font-family:ui-monospace,monospace;font-size:.8rem;color:#aaa;border:1px solid #555;border-radius:999px;padding:.18rem .48rem;letter-spacing:0}h2{font-size:1rem;text-transform:uppercase;letter-spacing:.08em;color:#bbb}
.card{border:1px solid #555;border-radius:12px;padding:1rem;margin:1rem 0;background:#171717}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem}
button{font:inherit;padding:.65rem .9rem;margin:.2rem;border:1px solid #777;border-radius:8px;background:#222;color:#fff}
button:hover{background:#333}button.danger{border-color:#aaa}
code,pre{background:#222;border-radius:6px}pre{padding:.8rem;overflow:auto;white-space:pre-wrap}
.muted{color:#aaa}.good{font-weight:700}.pill{display:inline-block;border:1px solid #666;border-radius:999px;padding:.2rem .55rem;margin:.15rem;font-size:.85rem}
nav{position:sticky;top:0;z-index:10;background:#111;padding:.55rem 0;border-bottom:1px solid #333;overflow-x:auto;white-space:nowrap}
nav a{display:inline-block;color:#ddd;text-decoration:none;padding:.5rem .7rem;border-radius:8px}
nav a:hover{background:#222}
.status-row{display:flex;gap:.5rem;flex-wrap:wrap;margin:.75rem 0}
.status-chip{border:1px solid #555;border-radius:999px;padding:.35rem .65rem;font-size:.9rem}
.action-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.5rem}
.action-grid button{width:100%;text-align:left;margin:0}
.action-grid small{display:block;color:#aaa;margin-top:.25rem}
.finding{border-left:3px solid #666;padding:.4rem .7rem;margin:.6rem 0}
.finding.attention{border-left-width:5px}
pre.raw{max-height:320px;overflow:auto;overscroll-behavior:contain;touch-action:pan-x pan-y}
#terminalOutput{max-height:50vh;overflow:auto;overscroll-behavior:contain;touch-action:pan-x pan-y;-webkit-overflow-scrolling:touch;white-space:pre-wrap;word-break:break-word}
.term-bold{font-weight:700}.term-fg-30{color:#777}.term-fg-31{color:#d88}.term-fg-32{color:#8d8}.term-fg-33{color:#dd8}.term-fg-34{color:#8ad}.term-fg-35{color:#d8d}.term-fg-36{color:#8dd}.term-fg-37{color:#ddd}
@media(max-width:600px){body{margin:1rem auto}.card{padding:.85rem}.grid{grid-template-columns:1fr}button{min-height:44px}}
</style>
</head>
<body>
<div class="brand-row"><h1>RELMOTE</h1><span id="headerVersion" class="brand-version">…</span></div>
<div class="muted">Help and diagnostics for this computer</div>
<nav>
<a href="#overview">Overview</a>
<a href="#diagnostics">Diagnostics</a>
<a href="#terminal">Terminal</a>
<a href="#help">Help</a>
<a href="#activity">Activity</a>
<a href="#about">About</a>
</nav>
<div id="actionStatus" class="card" style="display:none"></div>
<div id="startupError" class="card" style="display:none;border-color:#aaa"></div>

<div id="overview" class="grid">
 <section class="card"><h2>Node</h2><div id="node">Loading…</div></section>
 <section class="card"><h2>Target</h2><div id="target">Loading…</div></section>
 <section class="card"><h2>Session</h2><div id="session"></div></section>
</div>

<section class="card">
 <h2>Remote support</h2>
 <div id="supportState">Loading…</div>
 <button onclick="supportAction('until-disabled')">Enable until I turn it off</button>
 <button onclick="supportAction('one-hour')">Enable for 1 hour</button>
 <button class="danger" onclick="supportAction('disable')">Disable support</button>
 <p class="muted">This controls permission for remote support. It does not configure Tailscale, SSH, or network exposure by itself.</p>
</section>

<section id="terminal" class="card">
 <h2>Remote tools</h2>
 <div id="remoteTools">Loading…</div>
 <button id="requestScreenButton" onclick="requestScreen()">Request screen view</button>
 <div id="screenSessions"></div>
 <button id="requestTerminalButton" onclick="requestTerminal()">Request terminal on this computer</button>
 <div id="terminalSessions"></div>
 <div id="terminalPanel" style="display:none">
   <h3>Terminal</h3>
   <pre id="terminalOutput" style="min-height:240px;max-height:420px;overflow:auto"></pre>
   <form onsubmit="sendTerminal(event)">
     <label for="terminalInput">Input</label>
     <input id="terminalInput" autocomplete="off" style="width:100%;font:inherit;padding:.65rem;background:#111;color:#fff;border:1px solid #777;border-radius:8px">
   </form>
   <p class="muted">Preview terminal uses a normal-user local shell. Administrative terminal is not implemented.</p>
 </div>
</section>

<section id="agentAccess" class="card">
 <h2>Agent access</h2>
 <p class="muted">Create a scoped session for an external agent. The agent runs elsewhere; Relmote remains the target-side permission boundary.</p>
 <label for="agentWorkspace">Approved workspace</label>
 <input id="agentWorkspace" placeholder="/home/user/project" style="width:100%;font:inherit;padding:.65rem;background:#111;color:#fff;border:1px solid #777;border-radius:8px">
 <div style="margin:.7rem 0">
  <label><input id="agentList" type="checkbox" checked> List files</label><br>
  <label><input id="agentRead" type="checkbox" checked> Read files</label><br>
  <label><input id="agentExec" type="checkbox" checked> Run approved commands</label><br>
  <label><input type="checkbox" disabled> Modify files <span class="muted">(coming after read/exec validation)</span></label>
 </div>
 <button onclick="requestAgentAccess()">Create agent request</button>
 <div id="agentSessions"></div>
 <div id="agentCredential" class="card" style="display:none">
  <strong>Temporary agent credential</strong>
  <p class="muted">Shown after approval. Copy it to the external adapter, then keep it private.</p>
  <input id="agentToken" readonly style="width:100%;font:ui-monospace,monospace;padding:.65rem;background:#111;color:#fff;border:1px solid #777;border-radius:8px">
  <button onclick="copyAgentToken()">Copy credential</button>
 </div>
</section>

<section class="card">
 <h2>Capabilities</h2>
 <p class="muted">What this Relmote build can inspect or control. These are status labels, not buttons.</p>
 <div id="caps"></div>
</section>

<section id="diagnostics" class="card">
 <h2>Diagnostics</h2>
 <button onclick="runTask('full-check')"><strong>Run Full Check</strong></button>
 <p class="muted">Looks at system, storage, services, and network configuration without changing anything.</p>
 <details open><summary>Focused checks</summary>
 <div class="action-grid">
  <button onclick="runTask('system-overview')"><strong>System</strong><small>Identity, platform, memory and storage</small></button>
  <button onclick="runTask('network-overview')"><strong>Network</strong><small>Configured addresses and interfaces</small></button>
  <button onclick="runTask('diagnose-network')"><strong>Network diagnosis</strong><small>DNS and network configuration findings</small></button>
  <button onclick="runTask('storage-overview')"><strong>Storage</strong><small>Filesystem capacity and utilization</small></button>
  <button onclick="selfCheck()"><strong>Relmote self-check</strong><small>Verify Relmote's own local capabilities</small></button>
 </div>
 </details>
 <p class="muted">These checks only view information. They do not change this computer.</p>
</section>

<section id="help" class="card">
 <h2>Help</h2>
 <p class="muted">Choose a topic for plain-language guidance.</p>
 <button onclick="showHelp('getting-started')">Getting started</button>
 <button onclick="showHelp('support')">Support</button>
 <button onclick="showHelp('remote')">Remote access</button>
 <button onclick="showHelp('privacy')">Privacy</button>
 <pre id="helpText" class="muted"></pre>
</section>

<section id="about" class="card">
 <h2>About Relmote</h2>
 <div id="aboutInfo" class="muted">Loading…</div>
 <p>
  <a href="https://github.com/dev11systems/relmote" target="_blank" rel="noopener">GitHub source</a> ·
  <a href="https://github.com/dev11systems/relmote/issues" target="_blank" rel="noopener">Report an issue</a> ·
  <a href="https://github.com/dev11systems/relmote/blob/main/CHANGELOG.md" target="_blank" rel="noopener">Full changelog</a>
 </p>
 <details><summary>What's changed in this snapshot</summary>
  <pre id="changelogText" class="raw"></pre>
 </details>
</section>

<section class="card">
 <h2>Preview tools</h2>
 <button onclick="exportReport()">Export support report</button>
 <p id="previewStatus" class="muted"></p>
</section>

<section id="activity" class="card">
 <h2>Results & activity</h2>
 <p class="muted">Recent checks appear here with conclusions first. Expand evidence only when you need it.</p>
 <div id="tasks" class="muted">No observations yet.</div>
</section>

<p class="muted">Network exposure follows the active Relmote connection policy. Automatic mode prefers a private Tailscale interface when available and otherwise stays localhost-only. Controller pairing is still under development.</p>

<script>
const relmoteToken=new URLSearchParams(location.search).get('token');
const nodeEl=document.getElementById('node');
const targetEl=document.getElementById('target');
const sessionEl=document.getElementById('session');
const supportStateEl=document.getElementById('supportState');
const remoteToolsEl=document.getElementById('remoteTools');
const terminalSessionsEl=document.getElementById('terminalSessions');
const screenSessionsEl=document.getElementById('screenSessions');
const terminalPanelEl=document.getElementById('terminalPanel');
const terminalOutputEl=document.getElementById('terminalOutput');
const terminalInputEl=document.getElementById('terminalInput');
const agentWorkspaceEl=document.getElementById('agentWorkspace');
const agentSessionsEl=document.getElementById('agentSessions');
const agentCredentialEl=document.getElementById('agentCredential');
const agentTokenEl=document.getElementById('agentToken');
const capsEl=document.getElementById('caps');
const tasksEl=document.getElementById('tasks');
const helpTextEl=document.getElementById('helpText');
const previewStatusEl=document.getElementById('previewStatus');
const startupErrorEl=document.getElementById('startupError');
const ansiState={fg:null,bold:false};
function terminalHtml(text){
 let out='';
 let i=0;
 while(i<text.length){
   if(text.charCodeAt(i)===27){
     if(text[i+1]==='['){
       const end=text.indexOf('m',i+2);
       if(end!==-1){
         const codes=text.slice(i+2,end).split(';').filter(Boolean).map(Number);
         if(!codes.length) codes.push(0);
         for(const code of codes){
           if(code===0){ansiState.fg=null;ansiState.bold=false}
           else if(code===1){ansiState.bold=true}
           else if(code>=30&&code<=37){ansiState.fg=code}
           else if(code===39){ansiState.fg=null}
         }
         i=end+1; continue;
       }
       const match=text.slice(i).match(/^\x1b\[[0-9;?]*[A-Za-z]/);
       if(match){i+=match[0].length;continue}
     }else if(text[i+1]===']'){
       let end=text.indexOf('\x07',i+2);
       let width=1;
       const st=text.indexOf('\x1b\\',i+2);
       if(st!==-1&&(end===-1||st<end)){end=st;width=2}
       if(end!==-1){i=end+width;continue}
     }
     i++; continue;
   }
   let j=i;
   while(j<text.length&&text.charCodeAt(j)!==27)j++;
   const chunk=esc(text.slice(i,j));
   const cls=(ansiState.bold?' term-bold':'')+(ansiState.fg?' term-fg-'+ansiState.fg:'');
   out+='<span class="'+cls.trim()+'">'+chunk+'</span>';
   i=j;
 }
 return out;
}
const aboutInfoEl=document.getElementById('aboutInfo');
const headerVersionEl=document.getElementById('headerVersion');
const changelogTextEl=document.getElementById('changelogText');
const actionStatusEl=document.getElementById('actionStatus');
function showStatus(message,isError=false){
 actionStatusEl.style.display='block';
 actionStatusEl.textContent=message;
 actionStatusEl.style.borderColor=isError?'#aaa':'#666';
}
function clearStatus(){actionStatusEl.style.display='none';}
async function request(path, method='GET'){
 const headers={};
 if(relmoteToken) headers['X-Relmote-Token']=relmoteToken;
 const r=await fetch(path,{method,headers});
 const data=await r.json();
 if(!r.ok) throw new Error(data.error || r.statusText);
 return data;
}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
async function refresh(){
 const d=await request('/api/v1/snapshot');
 nodeEl.innerHTML='<strong>'+esc(d.node.name)+'</strong><br><code>'+esc(d.node.fingerprint)+'</code><br><span class="muted">'+esc(d.node.implementation)+'</span>';
 targetEl.innerHTML='<strong>'+esc(d.target.name)+'</strong><br><span class="muted">'+esc(d.target.relationship)+'</span>';
 capsEl.innerHTML=d.capabilities.map(x=>'<span class="pill">'+esc(d.capability_labels[x]||x)+'</span>').join('');
 const remote=d.support||{available:false,mode:'disabled'};
 supportStateEl.innerHTML='<strong>'+(remote.available?'ON':'OFF')+'</strong><br><span class="muted">'+esc(remote.mode)+'</span>';
 const features=d.features||{};
 const screen=features.screen||{};
 const terminal=features.terminal||{};
 remoteToolsEl.innerHTML=
   '<p><strong>Screen</strong><br>'+
   (screen.available?'Available':'Not available yet')+
   '<br><span class="muted">'+esc(screen.note||'')+'</span>'+
   (screen.session_type==='wayland'
     ? '<br><span class="muted">Portal: '+esc(screen.portal_ready?'Ready':(screen.portal_note||'Unavailable'))+'</span>'
     : '')+'</p>'+
   '<p><strong>Terminal</strong><br>'+
   (terminal.interactive_web_implemented?'Available':
     (terminal.available?'Transport detected · web terminal coming next':'Unavailable'))+
   '<br><span class="muted">'+esc(terminal.note||'')+'</span></p>';
 const agentItems=d.agent_sessions||[];
 agentSessionsEl.innerHTML=agentItems.length ? agentItems.map(a=>{
   let actions='';
   if(a.state==='requested'){
     actions='<button onclick="agentAction(\'approve\',\''+esc(a.session_id)+'\')">Allow agent</button>'+
             '<button class="danger" onclick="agentAction(\'revoke\',\''+esc(a.session_id)+'\')">Deny</button>';
   }else if(a.state==='active'){
     actions='<button class="danger" onclick="agentAction(\'revoke\',\''+esc(a.session_id)+'\')">Revoke</button>';
   }
   return '<div class="card"><strong>Agent · '+esc(a.state)+'</strong><br>'+
     'Workspace: <code>'+esc(a.workspace)+'</code><br>'+
     'Capabilities: '+esc(a.capabilities.join(', '))+'<br>'+actions+'</div>';
 }).join('') : '';
 const screenItems=d.screen_sessions||[];
 screenSessionsEl.innerHTML=screenItems.length ? screenItems.map(s=>{
   let actions='';
   if(s.state==='requested'){
     actions='<button onclick="screenAction(\'approve\',\''+esc(s.session_id)+'\')">Allow screen view</button>'+
             '<button onclick="screenAction(\'deny\',\''+esc(s.session_id)+'\')">Deny</button>';
   }else if(s.state==='os-consent'){
     actions='<span class="muted">Waiting for consent on target desktop.</span>';
   }else if(s.state==='active'){
     actions='<span class="good">Screen view active</span>';
   }else if(s.state==='failed'){
     actions='<span>Screen request failed.</span><br><span class="muted">'+esc(s.error||'Unknown portal error')+'</span>';
   }
   return '<div class="card"><strong>Screen · '+esc(s.state)+'</strong><br>'+
     'Controller: '+esc(s.controller)+'<br>Authority: '+esc(s.authority)+'<br>'+actions+'</div>';
 }).join('') : '';
 if(screenItems.some(s=>s.state==='os-consent')){
   setTimeout(()=>refresh().catch(()=>{}),1000);
 }
 const terminalItems=d.terminal_sessions||[];
 terminalSessionsEl.innerHTML=terminalItems.length ? terminalItems.map(t=>{
   let actions='';
   if(t.state==='requested'){
     actions='<button onclick="terminalAction(\'approve\',\''+esc(t.session_id)+'\')">Allow terminal</button>'+
             '<button onclick="terminalAction(\'deny\',\''+esc(t.session_id)+'\')">Deny</button>';
   }else if(t.state==='active'){
     actions='<button onclick="openTerminal(\''+esc(t.session_id)+'\')">Open terminal</button>'+
             '<button class="danger" onclick="terminalAction(\'end\',\''+esc(t.session_id)+'\')">End terminal</button>';
   }
   return '<div class="card"><strong>Terminal · '+esc(t.state)+'</strong><br>'+
     'Controller: '+esc(t.controller)+'<br>Authority: '+esc(t.authority)+'<br>'+actions+'</div>';
 }).join('') : '';
 if(!d.session || d.session.revoked){
   sessionEl.innerHTML='<strong>Local checks are off</strong><br><button onclick="startSession()">Enable checks</button>';
 }else{
   sessionEl.innerHTML='<span class="good">Local checks enabled</span><br><span class="muted">View information only</span><br><button class="danger" onclick="revoke()">Stop checks</button>';
 }
 if(d.tasks.length){
   tasksEl.innerHTML=d.tasks.slice().reverse().map(t=>{
     const findings=(t.findings||[]).map(f =>
       '<div class="finding '+esc(f.status)+'"><strong>'+esc(f.status)+'</strong> · '+esc(f.statement)+
       (f.uncertainty?'<br><span class="muted">'+esc(f.uncertainty)+'</span>':'')+'</div>'
     ).join('');
     return '<div class="card"><strong>'+esc(t.task_type)+'</strong><br><span class="muted">'+esc(t.created_at)+'</span>'+
       findings+
       '<details><summary>Evidence / raw observations</summary><pre class="raw">'+esc(JSON.stringify(t.observations,null,2))+'</pre></details></div>';
   }).join('');
 }else tasksEl.textContent='No observations yet.';
}
let activeTerminalId=null;
let terminalPoll=null;
async function requestAgentAccess(){
 const capabilities=[];
 if(document.getElementById('agentList').checked) capabilities.push('workspace.list');
 if(document.getElementById('agentRead').checked) capabilities.push('workspace.read');
 if(document.getElementById('agentExec').checked) capabilities.push('terminal.exec');
 try{
   await requestBody('/api/v1/controller/agent/request','POST',{
     workspace:agentWorkspaceEl.value,
     capabilities:capabilities,
     controller:'web-controller'
   });
   await refresh();
 }catch(e){showStatus('Agent request failed: '+e.message,true)}
}
async function agentAction(action,id){
 try{
   const value=await requestBody('/api/v1/controller/agent/'+encodeURIComponent(id)+'/'+action,'POST',{});
   if(action==='approve'&&value.token){
     agentTokenEl.value=value.token;
     agentCredentialEl.style.display='block';
   }
   await refresh();
 }catch(e){showStatus('Agent action failed: '+e.message,true)}
}
async function copyAgentToken(){
 try{
   await navigator.clipboard.writeText(agentTokenEl.value);
   showStatus('Agent credential copied.');
 }catch(e){showStatus('Could not copy credential: '+e.message,true)}
}
async function requestScreen(){
 try{
   await request('/api/v1/screen/request','POST');
   await refresh();
 }catch(e){showStatus('Screen request failed: '+e.message,true)}
}
async function screenAction(action,id){
 try{
   showStatus(action==='approve'?'Preparing screen consent…':'Updating screen request…');
   await request('/api/v1/screen/'+encodeURIComponent(id)+'/'+encodeURIComponent(action),'POST');
   await refresh();
 }catch(e){showStatus('Screen action failed: '+e.message,true)}
}
async function requestTerminal(){
 try{
   await request('/api/v1/terminal/request-local','POST');
   await refresh();
 }catch(e){alert(e.message)}
}
async function openTerminal(id){
 activeTerminalId=id;
 terminalPanelEl.style.display='block';
 terminalOutputEl.textContent='';
 if(terminalPoll) clearInterval(terminalPoll);
 await pollTerminal();
 terminalPoll=setInterval(pollTerminal,300);
 terminalInputEl.focus();
}
async function pollTerminal(){
 if(!activeTerminalId) return;
 try{
   const d=await request('/api/v1/terminal/'+encodeURIComponent(activeTerminalId)+'/read');
   if(d.data){
     const bytes=Uint8Array.from(atob(d.data),c=>c.charCodeAt(0));
     const decoded=new TextDecoder().decode(bytes);
     terminalOutputEl.insertAdjacentHTML('beforeend',terminalHtml(decoded));
     terminalOutputEl.scrollTop=terminalOutputEl.scrollHeight;
   }
 }catch(e){
   if(terminalPoll) clearInterval(terminalPoll);
 }
}
async function sendTerminal(event){
 event.preventDefault();
 if(!activeTerminalId) return;
 const value=terminalInputEl.value+'\n';
 terminalInputEl.value='';
 const bytes=new TextEncoder().encode(value);
 let binary=''; bytes.forEach(b=>binary+=String.fromCharCode(b));
 await requestBody('/api/v1/terminal/'+encodeURIComponent(activeTerminalId)+'/write','POST',{data:btoa(binary)});
}
async function requestBody(path,method,body){
 const headers={'Content-Type':'application/json'};
 if(relmoteToken) headers['X-Relmote-Token']=relmoteToken;
 const r=await fetch(path,{method,headers,body:JSON.stringify(body)});
 const data=await r.json();
 if(!r.ok) throw new Error(data.error||r.statusText);
 return data;
}
async function terminalAction(action,id){
 try{
   showStatus(action==='approve'?'Starting terminal…':'Updating terminal request…');
   await request('/api/v1/terminal/'+encodeURIComponent(id)+'/'+encodeURIComponent(action),'POST');
   await refresh();
   showStatus(action==='approve'?'Terminal approved. Choose Open terminal.':'Terminal request updated.');
 }catch(e){
   showStatus('Terminal action failed: '+e.message,true);
 }
}
async function supportAction(action){
 await request('/api/v1/support/'+encodeURIComponent(action),'POST');
 await refresh();
}
async function startSession(){await request('/api/v1/session','POST');await refresh()}
async function revoke(){await request('/api/v1/session/revoke','POST');await refresh()}
async function runTask(name){
 try{await request('/api/v1/tasks/'+encodeURIComponent(name),'POST');await refresh()}
 catch(e){alert(e.message)}
}
async function selfCheck(){
 try{
   const d=await request('/api/v1/self-check');
   previewStatusEl.textContent='Self-check: '+d.status+' · '+JSON.stringify(d.checks);
 }catch(e){alert(e.message)}
}
async function showHelp(topic){
 try{
   const d=await request('/api/v1/help/'+encodeURIComponent(topic));
   helpTextEl.textContent=d.text;
 }catch(e){alert(e.message)}
}
async function exportReport(){
 try{
   const d=await request('/api/v1/export','POST');
   previewStatusEl.textContent='Report written to: '+d.path+' — inspect before sharing.';
 }catch(e){alert(e.message)}
}
request('/api/v1/project').then(p=>{
 headerVersionEl.textContent=p.build.display_version;
 aboutInfoEl.textContent=p.build.display_version+' · build '+p.build.short_commit;
 changelogTextEl.textContent=p.changelog;
}).catch(()=>{});
refresh().catch(e=>{
 startupErrorEl.style.display='block';
 startupErrorEl.textContent='Relmote could not load runtime data: '+e.message;
});
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


def _parse_terminal_path(path: str) -> tuple[str, str] | None:
    parts = path.strip("/").split("/")
    # /api/v1/terminal/<session-id>/<action>
    if len(parts) != 5 or parts[:3] != ["api", "v1", "terminal"]:
        return None
    return parts[3], parts[4]


def make_handler(node: SoftwareNode, lan_access: TemporaryLANAccess | None = None, runtime: RelmoteRuntime | None = None):
    def authorized(handler: BaseHTTPRequestHandler) -> bool:
        if lan_access is None:
            return True
        parsed = urlparse(handler.path)
        token = parse_qs(parsed.query).get("token", [None])[0]
        if token is None:
            token = handler.headers.get("X-Relmote-Token")
        return lan_access.valid(token)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if not authorized(self):
                _json(self, HTTPStatus.UNAUTHORIZED, {"error": "temporary LAN token required"})
                return
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
                value = runtime.snapshot() if runtime else node.snapshot()
                value["capability_labels"] = {
                    cap: capability_label(cap) for cap in value["capabilities"]
                }
                _json(self, HTTPStatus.OK, value)
            elif path == "/api/v1/health":
                _json(self, HTTPStatus.OK, {"status": "ok"})
            elif path.startswith("/api/v1/terminal/") and path.endswith("/read"):
                if not runtime:
                    _json(self, HTTPStatus.BAD_REQUEST, {"error": "terminal runtime unavailable"})
                else:
                    parsed_terminal = _parse_terminal_path(path)
                    if parsed_terminal is None:
                        _json(self, HTTPStatus.BAD_REQUEST, {"error": "invalid terminal read path"})
                        return
                    session_id, action = parsed_terminal
                    if action != "read":
                        _json(self, HTTPStatus.BAD_REQUEST, {"error": "invalid terminal read action"})
                        return
                    data = runtime.read_terminal(session_id)
                    _json(self, HTTPStatus.OK, {
                        "data": base64.b64encode(data).decode("ascii"),
                    })
            elif path == "/api/v1/project":
                info = build_info()
                _json(self, HTTPStatus.OK, {
                    "build": info,
                    "project_url": PROJECT_URL,
                    "issues_url": ISSUES_URL,
                    "changelog_url": CHANGELOG_URL,
                    "changelog": bundled_changelog(),
                })
            elif path == "/api/v1/self-check":
                _json(self, HTTPStatus.OK, node.self_check())
            elif path.startswith("/api/v1/help/"):
                topic = path.rsplit("/", 1)[-1]
                try:
                    text_value = render_help(topic)
                except ValueError as exc:
                    _json(self, HTTPStatus.BAD_REQUEST, {"error": str(exc)})
                else:
                    _json(self, HTTPStatus.OK, {"topic": topic, "text": text_value})
            else:
                _json(self, HTTPStatus.NOT_FOUND, {"error": "not found"})

        def do_POST(self):
            if not authorized(self):
                _json(self, HTTPStatus.UNAUTHORIZED, {"error": "temporary LAN token required"})
                return
            path = urlparse(self.path).path
            try:
                if path.startswith("/api/v1/controller/agent"):
                    if not runtime:
                        raise ValueError("agent lifecycle requires shared runtime")
                    length = int(self.headers.get("Content-Length", "0"))
                    payload = json.loads(self.rfile.read(length) or b"{}")
                    status, value = agent_controller_handle(runtime, path, payload)
                    _json(self, HTTPStatus(status), value)
                elif path == "/api/v1/screen/request":
                    if not runtime:
                        raise ValueError("screen lifecycle requires shared runtime")
                    session = runtime.request_screen(controller="web-controller")
                    _json(self, HTTPStatus.CREATED, {
                        "session_id": session.session_id,
                        "state": session.state.value,
                    })
                elif path.startswith("/api/v1/screen/"):
                    if not runtime:
                        raise ValueError("screen lifecycle requires shared runtime")
                    parts = path.strip("/").split("/")
                    if len(parts) != 5:
                        raise ValueError("invalid screen action path")
                    session_id, action = parts[3], parts[4]
                    if action == "approve":
                        runtime.approve_screen(session_id)
                    elif action == "deny":
                        runtime.deny_screen(session_id)
                    elif action == "end":
                        runtime.end_screen(session_id)
                    else:
                        raise ValueError("unknown screen action")
                    _json(self, HTTPStatus.OK, runtime.snapshot())
                elif path == "/api/v1/terminal/request-local":
                    if not runtime:
                        raise ValueError("terminal lifecycle requires shared runtime")
                    session = runtime.request_terminal(
                        "this-computer",
                        controller="web-controller",
                    )
                    _json(self, HTTPStatus.CREATED, {
                        "session_id": session.session_id,
                        "state": session.state.value,
                    })
                elif path.startswith("/api/v1/terminal/"):
                    if not runtime:
                        raise ValueError("terminal lifecycle requires shared runtime")
                    parsed_terminal = _parse_terminal_path(path)
                    if parsed_terminal is None:
                        raise ValueError("invalid terminal action path")
                    session_id, action = parsed_terminal
                    if action == "write":
                        length = int(self.headers.get("Content-Length", "0"))
                        payload = json.loads(self.rfile.read(length) or b"{}")
                        raw = base64.b64decode(payload.get("data", ""), validate=True)
                        runtime.write_terminal(session_id, raw)
                        _json(self, HTTPStatus.OK, {"written": len(raw)})
                    elif action == "approve":
                        runtime.approve_terminal(session_id)
                    elif action == "deny":
                        runtime.deny_terminal(session_id)
                    elif action == "end":
                        runtime.end_terminal(session_id)
                    else:
                        raise ValueError("unknown terminal action")
                    _json(self, HTTPStatus.OK, runtime.snapshot())
                elif path.startswith("/api/v1/support/"):
                    if not runtime:
                        raise ValueError("support policy requires shared runtime")
                    action = path.rsplit("/", 1)[-1]
                    if action == "until-disabled":
                        runtime.enable_support_until_disabled()
                    elif action == "one-hour":
                        runtime.enable_support_for(3600)
                    elif action == "disable":
                        runtime.disable_support()
                    else:
                        raise ValueError("unknown support action")
                    _json(self, HTTPStatus.OK, runtime.snapshot())
                elif path == "/api/v1/session":
                    if runtime:
                        value = runtime.start_checks()
                        session = value["session"]
                        _json(self, HTTPStatus.CREATED, {
                            "session_id": session["session_id"],
                            "mode": "observe",
                        })
                    else:
                        session = node.start_observe_session()
                        _json(self, HTTPStatus.CREATED, {
                            "session_id": session.session_id,
                            "mode": "observe",
                        })
                elif path == "/api/v1/session/revoke":
                    if runtime:
                        runtime.stop_checks()
                    else:
                        node.revoke_session()
                    _json(self, HTTPStatus.OK, {"revoked": True})
                elif path == "/api/v1/export":
                    destination = (
                        __import__("pathlib").Path(tempfile.gettempdir())
                        / "relmote-support-report.json"
                    )
                    written = export_support_report(node, destination)
                    _json(self, HTTPStatus.CREATED, {"path": str(written)})
                elif path.startswith("/api/v1/tasks/"):
                    task_type = path.rsplit("/", 1)[-1]
                    if runtime:
                        value = runtime.run_task(task_type)
                        task = value["tasks"][-1]
                        _json(self, HTTPStatus.CREATED, {
                            "task_id": task["task_id"],
                            "task_type": task["task_type"],
                        })
                    else:
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
            except (OSError, RuntimeError, KeyError) as exc:
                _json(self, HTTPStatus.INTERNAL_SERVER_ERROR, {
                    "error": f"{type(exc).__name__}: {exc}",
                })

        def log_message(self, format, *args):
            return

    return Handler


def _best_lan_address() -> str:
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("192.0.2.1", 9))
        return probe.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())
    finally:
        probe.close()


def serve_local(
    host: str = "127.0.0.1",
    port: int = 8787,
    *,
    lan: bool = False,
    lifetime_minutes: int = 60,
    runtime: RelmoteRuntime | None = None,
    explicit_private_bind: bool = False,
    explicit_lan_bind: bool = False,
    access_token: str | None = None,
) -> None:
    if lan or explicit_lan_bind:
        host = "0.0.0.0"
        access = TemporaryLANAccess.create(
            lifetime_seconds=lifetime_minutes * 60
        )
    else:
        if (
            host not in {"127.0.0.1", "::1", "localhost"}
            and not explicit_private_bind
        ):
            raise ValueError(
                "non-loopback binding requires an explicit private or LAN exposure mode"
            )
        access = None

    if access_token:
        class FixedAccess:
            token = access_token
            def valid(self, candidate):
                return bool(candidate) and secrets.compare_digest(candidate, self.token)
        access = FixedAccess()

    runtime = runtime or RelmoteRuntime()
    node = runtime.node
    server = ThreadingHTTPServer(
        (host, port),
        make_handler(node, access, runtime),
    )
    if access:
        address = _best_lan_address()
        print("Relmote LAN PREVIEW (trusted private LAN only)")
        print(f"http://{address}:{port}/?token={access.token}")
        print(f"expires in {lifetime_minutes} minutes")
    else:
        print(f"Relmote: http://{host}:{port}")
    print(f"Node fingerprint: {node.identity.fingerprint}")
    print("Read-only software node. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.revoke_session()
        server.server_close()
