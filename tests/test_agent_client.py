import urllib.error
from unittest.mock import patch

import pytest

from relmote.agent_client import RelmoteAgentClient, pair


def test_agent_request_formats_unreachable_target():
    client = RelmoteAgentClient(
        "http://100.64.1.2:8788",
        "test-token",
    )

    with patch(
        "relmote.agent_client.urllib.request.urlopen",
        side_effect=urllib.error.URLError("connection refused"),
    ):
        with pytest.raises(
            ConnectionError,
            match="Relmote Agent API unavailable: connection refused",
        ):
            client.session()


def test_pair_formats_unreachable_endpoint():
    with patch(
        "relmote.agent_client.urllib.request.urlopen",
        side_effect=urllib.error.URLError("connection refused"),
    ):
        with pytest.raises(
            ConnectionError,
            match="Relmote pairing endpoint unavailable: connection refused",
        ):
            pair("http://100.64.1.2:8788", "12345678")


def test_agent_info_uses_authenticated_read_only_endpoint():
    client = RelmoteAgentClient(
        "http://100.64.1.2:8788",
        "test-token",
    )

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"role":"target","session":{"state":"active"}}'

    with patch(
        "relmote.agent_client.urllib.request.urlopen",
        return_value=Response(),
    ) as open_url:
        value = client.info()

    request = open_url.call_args.args[0]
    assert request.full_url.endswith("/api/v1/agent/info")
    assert request.method == "GET"
    assert request.get_header("Authorization") == "Bearer test-token"
    assert value["role"] == "target"
