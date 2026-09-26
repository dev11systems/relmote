from unittest.mock import patch

import pytest

from relmote.network_exposure import ExposureMode, choose_exposure


@patch("relmote.network_exposure.tailscale_ipv4", return_value="100.64.1.2")
def test_auto_prefers_tailscale_only(mock_ts):
    choice = choose_exposure("auto")

    assert choice.mode is ExposureMode.TAILSCALE
    assert choice.bind_host == "100.64.1.2"
    assert choice.private


@patch("relmote.network_exposure.tailscale_ipv4", return_value=None)
def test_auto_falls_back_to_localhost_not_all_interfaces(mock_ts):
    choice = choose_exposure("auto")

    assert choice.mode is ExposureMode.LOCALHOST
    assert choice.bind_host == "127.0.0.1"


def test_lan_requires_explicit_choice():
    choice = choose_exposure("lan")

    assert choice.bind_host == "0.0.0.0"
    assert choice.private is False


@patch("relmote.network_exposure.tailscale_ipv4", return_value=None)
def test_explicit_tailscale_fails_if_unavailable(mock_ts):
    with pytest.raises(RuntimeError, match="not connected"):
        choose_exposure("tailscale")
