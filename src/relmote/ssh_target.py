from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SSHCommandResult:
    target: str
    probe: str
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class SSHTarget:
    """Read-only preview adapter using the host OpenSSH client.

    S3 deliberately exposes named probes rather than arbitrary command strings.
    Authentication, host-key checking, ProxyJump, and Tailscale addressing stay
    in the user's existing SSH configuration.
    """

    PROBES: dict[str, tuple[str, ...]] = {
        "identity": ("uname", "-a"),
        "hostname": ("hostname",),
        "uptime": ("uptime",),
        "disk": ("df", "-h"),
        "memory-linux": ("free", "-h"),
        "network-linux": ("ip", "address", "show"),
        "routes-linux": ("ip", "route", "show"),
    }

    def __init__(
        self,
        target: str,
        *,
        ssh_binary: str = "ssh",
        connect_timeout: int = 10,
        extra_options: Sequence[str] = (),
    ) -> None:
        if not target:
            raise ValueError("SSH target is required")
        if connect_timeout <= 0:
            raise ValueError("connect_timeout must be positive")
        self.target = target
        self.ssh_binary = ssh_binary
        self.connect_timeout = connect_timeout
        self.extra_options = tuple(extra_options)

    def run_probe(self, probe: str) -> SSHCommandResult:
        command = self.PROBES.get(probe)
        if command is None:
            raise ValueError(f"unsupported SSH probe: {probe}")

        argv = [
            self.ssh_binary,
            "-o", "BatchMode=yes",
            "-o", f"ConnectTimeout={self.connect_timeout}",
            *self.extra_options,
            self.target,
            "--",
            *command,
        ]
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=self.connect_timeout + 5,
            check=False,
        )
        return SSHCommandResult(
            target=self.target,
            probe=probe,
            command=command,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    @classmethod
    def available_probes(cls) -> tuple[str, ...]:
        return tuple(sorted(cls.PROBES))
