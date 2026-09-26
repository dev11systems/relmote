from __future__ import annotations

import base64
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Sequence

from .workspace import WorkspacePolicy


@dataclass(frozen=True)
class WorkspaceResult:
    operation: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class SSHWorkspace:
    """Read-only workspace executor over an existing OpenSSH path.

    This preview does not accept arbitrary shell strings.
    """

    def __init__(
        self,
        target: str,
        policy: WorkspacePolicy,
        *,
        ssh_binary: str = "ssh",
        connect_timeout: int = 10,
        extra_options: Sequence[str] = (),
    ) -> None:
        self.target = target
        self.policy = policy
        self.ssh_binary = ssh_binary
        self.connect_timeout = connect_timeout
        self.extra_options = tuple(extra_options)

    def _run(self, operation: str, argv: list[str]) -> WorkspaceResult:
        command = [
            self.ssh_binary,
            "-o", "BatchMode=yes",
            "-o", f"ConnectTimeout={self.connect_timeout}",
            *self.extra_options,
            self.target,
            "--",
            *argv,
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=self.connect_timeout + 30,
            check=False,
        )
        return WorkspaceResult(
            operation=operation,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    def list(self, relative: str = ".") -> WorkspaceResult:
        path = self.policy.resolve_relative(relative)
        # find is invoked directly through SSH argv, not through a local shell.
        return self._run(
            "list",
            ["find", str(path), "-maxdepth", "1", "-mindepth", "1", "-printf", "%f\n"],
        )

    def read(self, relative: str) -> WorkspaceResult:
        path = self.policy.resolve_relative(relative)
        return self._run("read", ["cat", "--", str(path)])

    def git_status(self) -> WorkspaceResult:
        self.policy.require_tool("git")
        return self._run(
            "git-status",
            ["git", "-C", str(self.policy.root), "status", "--short"],
        )

    def git_diff(self) -> WorkspaceResult:
        self.policy.require_tool("git")
        return self._run(
            "git-diff",
            ["git", "-C", str(self.policy.root), "diff", "--"],
        )

    def run_tool(self, tool: str, args: Sequence[str] = ()) -> WorkspaceResult:
        self.policy.require_tool(tool)
        if tool == "git":
            raise ValueError("use explicit git_status/git_diff operations in preview")
        # Tool name comes from policy; args are passed as argv, never shell-concatenated.
        return self._run(
            f"tool:{tool}",
            [tool, *args],
        )
