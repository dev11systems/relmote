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
