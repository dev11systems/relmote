from unittest.mock import patch

import pytest

from relmote.ssh_target import SSHTarget


def test_preview_exposes_named_read_only_probes():
    probes = SSHTarget.available_probes()

    assert "identity" in probes
    assert "disk" in probes
    assert "shell" not in probes


def test_unknown_probe_is_rejected_before_ssh():
    target = SSHTarget("example")

    with pytest.raises(ValueError, match="unsupported SSH probe"):
        target.run_probe("rm-everything")


@patch("relmote.ssh_target.subprocess.run")
def test_probe_uses_batch_mode_and_existing_ssh(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "host\n"
    mock_run.return_value.stderr = ""

    result = SSHTarget("cousin-host").run_probe("hostname")

    argv = mock_run.call_args.args[0]
    assert argv[0] == "ssh"
    assert "BatchMode=yes" in argv
    assert "cousin-host" in argv
    assert result.ok
    assert result.stdout == "host\n"
