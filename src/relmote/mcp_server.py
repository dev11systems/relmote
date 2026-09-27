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

RELMOTE_MCP_INSTRUCTIONS = """
This MCP server runs on a Relmote Agent Host.

Role model:
- The Agent Host is the local machine running Codex and relmote-mcp.
- A tool argument named target identifies a paired Relmote Target.
- A Target is separate from the Agent Host unless the human explicitly paired
  that same machine as a target.
- Paths returned by target tools belong to the Target's approved workspace,
  not to the Agent Host filesystem.
- relmote_list, relmote_read, and relmote_exec operate on the named Target.
- This MCP server does not expose the Agent Host local filesystem as a target.

Authority:
- Connectivity does not imply authority.
- Target-side capabilities, workspace confinement, revocation, and transport
  availability are authoritative.
- If a Relmote tool is denied or revoked, do not bypass that denial by using
  local shell, SSH, Tailscale, another network path, or another tool unless
  the human explicitly asks for a separate non-Relmote workflow.

When reporting results, clearly distinguish the Agent Host from the Target.
""".strip()


class RelmoteMCPTools:
    """Credential-blind MCP-facing operations over paired Relmote targets."""

    def __init__(self, service: PairedTargetService | None = None):
        self.service = service or PairedTargetService()

    @staticmethod
    def context() -> dict[str, Any]:
        return {
            "this_process_role": "agent_host",
            "target_argument_role": "paired_target",
            "target_paths_belong_to": "target_workspace",
            "target_execution_location": "target",
            "agent_host_filesystem_exposed_as_target": False,
            "authority_rule": (
                "Target-side grants, workspace confinement, revocation, and "
                "transport availability remain authoritative."
            ),
            "bypass_rule": (
                "A Relmote denial is not permission to bypass Relmote with "
                "local shell, SSH, Tailscale, or another transport."
            ),
        }

    @staticmethod
    def _target_context(target: str) -> dict[str, Any]:
        return {
            "agent_host_role": "local_agent_host",
            "target_role": "paired_target",
            "target": target,
            "execution_location": "target",
        }

    def targets(self) -> dict[str, Any]:
        targets = []
        for item in self.service.targets():
            value = dict(item)
            value["role"] = "paired_target"
            value["workspace_location"] = "target"
            targets.append(value)
        return {
            "context": self.context(),
            "targets": targets,
        }

    def status(self, target: str) -> dict[str, Any]:
        return {
            "context": self._target_context(target),
            "target_status": self.service.status(target),
        }

    def list(self, target: str, path: str = ".") -> dict[str, Any]:
        return {
            "context": {
                **self._target_context(target),
                "path": path,
                "path_location": "target_workspace",
            },
            "entries": self.service.list(target, path),
        }

    def read(self, target: str, path: str) -> dict[str, Any]:
        return {
            "context": {
                **self._target_context(target),
                "path": path,
                "path_location": "target_workspace",
            },
            "text": self.service.read(target, path),
        }

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

        result = self.service.exec(
            target,
            argv,
            cwd=cwd,
            timeout=timeout,
        )
        return {
            "context": {
                **self._target_context(target),
                "cwd": cwd,
                "cwd_location": "target_workspace",
                "operation": operation,
            },
            "result": result,
        }


def build_mcp_server(
    service: PairedTargetService | None = None,
):
    if MCPServer is None:
        raise RuntimeError(MCP_INSTALL_HINT)

    tools = RelmoteMCPTools(service)
    server = MCPServer(
        "Relmote Agent Host",
        description=(
            "Credential-blind access from an Agent Host to separately paired "
            "Relmote Targets."
        ),
        instructions=RELMOTE_MCP_INSTRUCTIONS,
    )

    @server.tool()
    def relmote_context() -> dict[str, Any]:
        """Explain Agent Host vs Target roles and Relmote authority semantics."""
        return tools.context()

    @server.tool()
    def relmote_targets() -> dict[str, Any]:
        """List paired REMOTE TARGETS.

        The returned target workspaces are on those Targets, not on this local
        Agent Host. Credentials and stored endpoint URLs are not exposed.
        """
        return tools.targets()

    @server.tool()
    def relmote_target_status(target: str) -> dict[str, Any]:
        """Get live status for a named REMOTE TARGET.

        Returned workspace paths and capabilities belong to the Target.
        Revoked or unreachable Targets fail closed.
        """
        return tools.status(target)

    @server.tool()
    def relmote_list(
        target: str,
        path: str = ".",
    ) -> dict[str, Any]:
        """List a path on the named REMOTE TARGET.

        The path is resolved inside that Target's authorized workspace and is
        not a path on the local Agent Host.
        """
        return tools.list(target, path)

    @server.tool()
    def relmote_read(
        target: str,
        path: str,
    ) -> dict[str, Any]:
        """Read a text file from the named REMOTE TARGET.

        The path and returned content belong to the Target's authorized
        workspace, not the local Agent Host.
        """
        return tools.read(target, path)

    @server.tool()
    def relmote_exec(
        target: str,
        operation: Literal["git_status", "git_diff", "pytest"],
        args: list[str] | None = None,
        cwd: str = ".",
        timeout: int = 30,
    ) -> dict[str, Any]:
        """Run one narrowly named operation ON THE NAMED REMOTE TARGET.

        Execution happens in the Target's authorized workspace, not on the
        local Agent Host. git_status and git_diff accept no extra arguments.
        pytest may receive explicit pytest arguments. Target-side workspace,
        capability, and revocation policy remains authoritative. A denial must
        not be bypassed through another transport.
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
