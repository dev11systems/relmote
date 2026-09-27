from __future__ import annotations


def agent_access_javascript() -> str:
    return r"""
const relmoteAgentState=document.getElementById('agentAccessState');
if(relmoteAgentState) relmoteAgentState.textContent='Status: frontend loaded · checking transport…';

async function agentRequest(path,payload=null){
  const bridge=window['relmote'+'Controller'+'Request'];
  if(!bridge) throw new Error('controller bridge unavailable');
  return bridge(path,payload===null?'GET':'POST',payload);
}
function agentNotice(message,isError=false){
  const status=document.getElementById('previewStatus');
  if(status) status.textContent=message;
  if(isError && relmoteAgentState) relmoteAgentState.textContent='Status: error · '+message;
}

async function refreshAgentAccess(){
  try{
    const value=await agentRequest('/api/v1/controller/agent/status');
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
    agentNotice('Enabling private Agent Access…');
    await agentRequest('/api/v1/controller/agent/enable');
    await refreshAgentAccess();
    agentNotice('Agent Access enabled privately.');
  }catch(e){
    agentNotice('Could not enable Agent Access: '+e.message,true);
  }
}
async function disableAgentAccess(){
  try{
    await agentRequest('/api/v1/controller/agent/disable');
    const credential=document.getElementById('agentCredential');
    const token=document.getElementById('agentToken');
    if(credential) credential.style.display='none';
    if(token) token.value='';
    await refreshAgentAccess();
    await refresh();
    agentNotice('Agent Access disabled and active grants revoked.');
  }catch(e){
    agentNotice('Could not disable Agent Access: '+e.message,true);
  }
}

refreshAgentAccess().catch(()=>{});
"""
