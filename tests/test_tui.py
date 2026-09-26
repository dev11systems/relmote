from relmote.runtime import RelmoteRuntime
from relmote.tui import render_home


def test_tui_uses_plain_language():
    text = render_home(RelmoteRuntime())

    assert "Check this computer" in text
    assert "Network diagnosis" in text
    assert "system.identify" not in text


def test_tui_reports_web_readiness():
    text = render_home(
        RelmoteRuntime(),
        web_url="http://127.0.0.1:9999",
        web_ready=True,
    )

    assert "Web interface: Ready" in text
    assert "http://127.0.0.1:9999" in text
