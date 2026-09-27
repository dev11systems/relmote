from __future__ import annotations


def agent_access_javascript() -> str:
    return r"""
async function refreshAgentAccess(){
  try{
    const value=await requestBody('/api/v1/controller/agent/status','POST',{});
    const on=!!value.enabled;
    document.getElementById('agentAccessState').textContent=
      'Status: '+(on?'ON · private transport ready':'OFF');
    document.getElementById('agentEnableButton').style.display=
      on?'none':'inline-block';
    document.getElementById('agentDisableButton').style.display=
      on?'inline-block':'none';
    document.getElementById('agentGrantSetup').style.display=
      on?'block':'none';
  }catch(e){
    document.getElementById('agentAccessState').textContent=
      'Status unavailable: '+e.message;
  }
}
async function enableAgentAccess(){
  try{
    showStatus('Enabling private Agent Access…');
    await requestBody('/api/v1/controller/agent/enable','POST',{});
    await refreshAgentAccess();
    showStatus('Agent Access enabled privately.');
  }catch(e){
    showStatus('Could not enable Agent Access: '+e.message,true);
  }
}
async function disableAgentAccess(){
  try{
    await requestBody('/api/v1/controller/agent/disable','POST',{});
    const credential=document.getElementById('agentCredential');
    const token=document.getElementById('agentToken');
    if(credential) credential.style.display='none';
    if(token) token.value='';
    await refreshAgentAccess();
    await refresh();
    showStatus('Agent Access disabled and active grants revoked.');
  }catch(e){
    showStatus('Could not disable Agent Access: '+e.message,true);
  }
}

refreshAgentAccess().catch(()=>{});
"""
