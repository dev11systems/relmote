from __future__ import annotations

import posixpath
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class WorkspacePolicy:
    root: PurePosixPath
    allowed_tools: frozenset[str] = frozenset({"git", "pytest"})
    writable: bool = False

    @classmethod
    def create(
        cls,
        root: str,
        *,
        allowed_tools: frozenset[str] | None = None,
        writable: bool = False,
    ) -> "WorkspacePolicy":
        path = PurePosixPath(root)
        if not path.is_absolute():
            raise ValueError("workspace root must be an absolute remote path")
        return cls(
            root=path,
            allowed_tools=allowed_tools or frozenset({"git", "pytest"}),
            writable=writable,
        )

    def resolve_relative(self, relative: str) -> PurePosixPath:
        if not relative:
            return self.root
        candidate = PurePosixPath(relative)
        if candidate.is_absolute():
            raise ValueError("workspace path must be relative")
        normalized = posixpath.normpath(str(candidate))
        if normalized == ".." or normalized.startswith("../"):
            raise ValueError("workspace path escapes configured root")
        return self.root / normalized

    def require_tool(self, tool: str) -> None:
        if tool not in self.allowed_tools:
            raise PermissionError(f"tool is not allowed by workspace policy: {tool}")

    def require_write(self) -> None:
        if not self.writable:
            raise PermissionError("workspace is read-only")
