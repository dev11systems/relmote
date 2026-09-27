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
