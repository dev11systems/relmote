import subprocess
from unittest.mock import patch

import pytest

from relmote.agent_access import enable_private_transport


def test_enable_private_transport_turns_tailscale_timeout_into_runtime_error():
    with patch("relmote.agent_access.tailscale_available", return_value=True), patch(
        "relmote.agent_access.subprocess.run",
        side_effect=subprocess.TimeoutExpired(
            cmd=["tailscale", "serve", "--bg", "8788"],
            timeout=30,
        ),
    ):
        with pytest.raises(RuntimeError, match="did not return within 30 seconds"):
            enable_private_transport()
