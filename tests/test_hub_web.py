from io import BytesIO
from unittest.mock import patch

from relmote.hub_web import HUB_INDEX, _authorized, make_hub_handler


class FakeAccess:
    def __init__(self, token="secret"):
        self.token = token

    def valid(self, candidate):
        return candidate == self.token


class FakeInventory:
    def snapshot(self, *, live=False):
        assert live is True
        return {
            "hub": {
                "role": "hub",
                "mode": "local-read-only",
                "authority": "inventory-only",
            },
            "agent_host": {
                "name": "agent-host-a",
                "platform": "linux",
                "architecture": "x86_64",
                "capabilities": [],
                "tools": [],
                "relmote": {
                    "display_version": "0.1.0-dev.12",
                    "short_commit": "abcdef12",
                },
            },
            "paired_targets": [],
            "summary": {
                "total": 0,
                "active": 0,
                "attention": 0,
                "revoked": 0,
                "stale_credential": 0,
                "unreachable": 0,
            },
        }


def test_hub_html_is_read_only_inventory_ui():
    assert "RELMOTE HUB" in HUB_INDEX
    assert "Read-only local inventory" in HUB_INDEX
    assert "/api/inventory" in HUB_INDEX
    assert "create Target grants" in HUB_INDEX
    assert "fetch('/api/inventory" in HUB_INDEX


def test_hub_token_auth_is_required_only_when_access_exists():
    assert _authorized(None, "/") is True
    access = FakeAccess()
    assert _authorized(access, "/?token=secret") is True
    assert _authorized(access, "/?token=wrong") is False
    assert _authorized(access, "/") is False


def test_hub_handler_exposes_no_write_api():
    handler = make_hub_handler(FakeInventory(), None)

    class Request:
        request_version = "HTTP/1.1"
        command = "POST"
        requestline = "POST /api/inventory HTTP/1.1"
        path = "/api/inventory"
        client_address = ("127.0.0.1", 12345)
        server = object()
        rfile = BytesIO()
        wfile = BytesIO()

        def send_response(self, code, message=None):
            self.status = code

        def send_header(self, key, value):
            pass

        def end_headers(self):
            pass

        def log_request(self, code="-", size="-"):
            pass

    # Instantiate without BaseHTTPRequestHandler.__init__ so no socket is needed.
    instance = object.__new__(handler)
    instance.path = Request.path
    instance.wfile = Request.wfile
    instance.send_response = Request.send_response.__get__(instance)
    instance.send_header = Request.send_header.__get__(instance)
    instance.end_headers = Request.end_headers.__get__(instance)
    instance.do_POST()

    body = instance.wfile.getvalue().decode()
    assert instance.status == 405
    assert "read-only" in body
