from __future__ import annotations

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

    File operations resolve the target-side canonical path before access so a
    symlink inside the configured root cannot silently escape it.
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

    def _canonical_remote(self, relative: str) -> PurePosixPath:
        lexical = self.policy.resolve_relative(relative)
        result = self._run(
            "resolve-path",
            ["realpath", "-e", "--", str(lexical)],
        )
        if not result.ok:
            raise FileNotFoundError(
                result.stderr.strip() or f"cannot resolve remote path: {relative}"
            )
        canonical = PurePosixPath(result.stdout.strip())
        root_result = self._run(
            "resolve-root",
            ["realpath", "-e", "--", str(self.policy.root)],
        )
        if not root_result.ok:
            raise FileNotFoundError("cannot resolve remote workspace root")
        canonical_root = PurePosixPath(root_result.stdout.strip())

        try:
            canonical.relative_to(canonical_root)
        except ValueError as exc:
            raise PermissionError(
                f"remote path escapes workspace through symlink: {relative}"
            ) from exc
        return canonical

    def list(self, relative: str = ".") -> WorkspaceResult:
        path = self._canonical_remote(relative)
        return self._run(
            "list",
            ["find", str(path), "-maxdepth", "1", "-mindepth", "1", "-printf", "%f\n"],
        )

    def read(self, relative: str) -> WorkspaceResult:
        path = self._canonical_remote(relative)
        return self._run("read", ["cat", "--", str(path)])

    def write_text(self, relative: str, content: str) -> WorkspaceResult:
        self.policy.require_write()
        lexical = self.policy.resolve_relative(relative)
        parent_relative = str(PurePosixPath(relative).parent)
        parent = self._canonical_remote(parent_relative)
        destination = parent / lexical.name

        # Transfer content on stdin to a tiny fixed remote program. The remote
        # argv contains the validated destination; content is never shell code.
        command = [
            self.ssh_binary,
            "-o", "BatchMode=yes",
            "-o", f"ConnectTimeout={self.connect_timeout}",
            *self.extra_options,
            self.target,
            "--",
            "python3",
            "-c",
            (
                "import os,pathlib,sys,tempfile;"
                "p=pathlib.Path(sys.argv[1]);"
                "fd,tmp=tempfile.mkstemp(prefix='.relmote-',dir=str(p.parent));"
                "f=os.fdopen(fd,'w');"
                "f.write(sys.stdin.read());f.flush();os.fsync(f.fileno());f.close();"
                "os.replace(tmp,p)"
            ),
            str(destination),
        ]
        completed = subprocess.run(
            command,
            input=content,
            capture_output=True,
            text=True,
            timeout=self.connect_timeout + 30,
            check=False,
        )
        return WorkspaceResult(
            operation="write-text",
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

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
        return self._run(
            f"tool:{tool}",
            [tool, *args],
        )
