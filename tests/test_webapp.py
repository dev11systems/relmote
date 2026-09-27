import pytest

from relmote.webapp import INDEX, _parse_terminal_path, serve_local
from relmote.web_agent_ui import agent_access_javascript


def test_non_loopback_requires_explicit_lan_mode():
    with pytest.raises(ValueError, match="explicit private or LAN"):
        serve_local(host="0.0.0.0", port=0)


def test_arbitrary_non_loopback_still_requires_explicit_exposure():
    with pytest.raises(ValueError, match="explicit private or LAN"):
        serve_local(host="192.0.2.10", port=0)


def test_rendered_web_ui_preserves_javascript_escapes():
    assert "terminalInputEl.value+'\\n'" in INDEX
    assert "terminalAction(\\'approve\\'" in INDEX
    assert "terminalAction(\\'deny\\'" in INDEX


def test_terminal_routes_have_one_consistent_shape():
    session_id = "abc-123"

    for action in ("approve", "deny", "end", "read", "write"):
        assert _parse_terminal_path(
            f"/api/v1/terminal/{session_id}/{action}"
        ) == (session_id, action)

    assert _parse_terminal_path("/api/v1/terminal/request-local") is None
    assert _parse_terminal_path("/api/v1/terminal/abc-123") is None


def test_rendered_web_ui_has_no_literal_source_newline_escape():
    assert "</button>\\n <div id=\"screenSessions\"" not in INDEX
    assert (
        "terminalSessions');\\nconst screenSessionsEl"
        not in INDEX
    )


def test_agent_access_javascript_is_external_and_renderable():
    assert '<script src="/relmote-agent.js"></script>' in INDEX
    assert "{agent_access_javascript()}" not in INDEX
    script = agent_access_javascript()
    assert "async function refreshAgentAccess()" in script
    assert "async function enableAgentAccess()" in script
    assert "async function disableAgentAccess()" in script


def test_agent_script_has_independent_fetch_helper():
    script = agent_access_javascript()
    assert "async function agentRequest(" in script
    assert "frontend loaded · checking transport" in script
    assert "requestBody('/api/v1/controller/agent/status'" not in script

def test_agent_lifecycle_actions_use_post_requests():
    script = agent_access_javascript()
    assert "agentRequest('/api/v1/controller/agent/enable',{})" in script
    assert "agentRequest('/api/v1/controller/agent/disable',{})" in script



def test_static_agent_script_does_not_require_controller_query_token():
    # Browser subresource requests do not inherit ?token= from the page URL.
    # The JS contains no target data/authority, so it must be loadable without
    # weakening authentication on controller API endpoints.
    source = __import__("inspect").getsource(
        __import__("relmote.webapp", fromlist=["make_handler"]).make_handler
    )
    static_pos = source.index('if path == "/relmote-agent.js"')
    auth_pos = source.index("if not authorized(self)", static_pos)
    assert static_pos < auth_pos
    assert "return" in source[static_pos:auth_pos]


def test_agent_module_uses_page_controller_bridge():
    script = agent_access_javascript()
    assert "controller bridge unavailable" in script
    assert "relmote'+'Controller'+'Request" in script
    # Authentication belongs to the page/controller layer, not this module.
    assert "X-Relmote-" not in script


def test_agent_disable_clears_stale_pairing_display():
    script = agent_access_javascript()
    assert "function clearAgentPairingDisplay()" in script
    assert "if(!on) clearAgentPairingDisplay();" in script
    disable_start = script.index("async function disableAgentAccess()")
    disable_end = script.index("refreshAgentAccess().catch", disable_start)
    assert "clearAgentPairingDisplay();" in script[disable_start:disable_end]
