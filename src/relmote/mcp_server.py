from __future__ import annotations

from typing import Any, Literal

from .paired_targets import PairedTargetService

try:
    from mcp.server import MCPServer
except ImportError:  # pragma: no cover - exercised by base installs without MCP.
    MCPServer = None


MCP_INSTALL_HINT = (
    "Relmote MCP support is not installed. "
    "Install the Agent Host with the 'mcp' extra."
)


class RelmoteMCPTools:
    """Credential-blind MCP-facing operations over paired Relmote targets."""

    def __init__(self, service: PairedTargetService | None = None):
        self.service = service or PairedTargetService()

    def targets(self) -> list[dict[str, Any]]:
        return self.service.targets()

    def status(self, target: str) -> dict[str, Any]:
        return self.service.status(target)

    def list(self, target: str, path: str = ".") -> list[dict[str, Any]]:
        return self.service.list(target, path)

    def read(self, target: str, path: str) -> str:
        return self.service.read(target, path)

    def exec(
        self,
        target: str,
        operation: Literal["git_status", "git_diff", "pytest"],
        *,
        args: list[str] | None = None,
        cwd: str = ".",
        timeout: int = 30,
    ) -> dict[str, Any]:
        extra = list(args or [])
        if operation == "git_status":
            if extra:
                raise ValueError("git_status does not accept extra arguments")
            argv = ["git", "status"]
        elif operation == "git_diff":
            if extra:
                raise ValueError("git_diff does not accept extra arguments")
            argv = ["git", "diff"]
        elif operation == "pytest":
            argv = ["pytest", *extra]
        else:  # Defensive for direct Python callers; MCP validates Literal.
            raise ValueError(f"unsupported MCP execution operation: {operation}")

        return self.service.exec(
            target,
            argv,
            cwd=cwd,
            timeout=timeout,
        )


def build_mcp_server(
    service: PairedTargetService | None = None,
):
    if MCPServer is None:
        raise RuntimeError(MCP_INSTALL_HINT)

    tools = RelmoteMCPTools(service)
    server = MCPServer("Relmote Agent Host")

    @server.tool()
    def relmote_targets() -> list[dict[str, Any]]:
        """List paired Relmote targets without exposing credentials or endpoints."""
        return tools.targets()

    @server.tool()
    def relmote_target_status(target: str) -> dict[str, Any]:
        """Get live target/session status; revoked or unreachable targets fail closed."""
        return tools.status(target)

    @server.tool()
    def relmote_list(
        target: str,
        path: str = ".",
    ) -> list[dict[str, Any]]:
        """List a path inside the target-authorized workspace."""
        return tools.list(target, path)

    @server.tool()
    def relmote_read(
        target: str,
        path: str,
    ) -> str:
        """Read a text file inside the target-authorized workspace."""
        return tools.read(target, path)

    @server.tool()
    def relmote_exec(
        target: str,
        operation: Literal["git_status", "git_diff", "pytest"],
        args: list[str] | None = None,
        cwd: str = ".",
        timeout: int = 30,
    ) -> dict[str, Any]:
        """Run one narrowly named operation when the target grants terminal.exec.

        git_status and git_diff accept no extra arguments. pytest may receive
        explicit pytest arguments. Target-side workspace and capability policy
        remains authoritative.
        """
        return tools.exec(
            target,
            operation,
            args=args,
            cwd=cwd,
            timeout=timeout,
        )

    return server


mcp = build_mcp_server() if MCPServer is not None else None


def main() -> int:
    if mcp is None:
        raise SystemExit(MCP_INSTALL_HINT)
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
