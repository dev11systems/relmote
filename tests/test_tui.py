from relmote.runtime import RelmoteRuntime
from relmote.tui import render_home


def test_tui_uses_plain_language():
    text = render_home(RelmoteRuntime())

    assert "Check this computer" in text
    assert "Network diagnosis" in text
    assert "system.identify" not in text
