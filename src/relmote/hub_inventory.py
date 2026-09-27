from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .agent_host import AgentHost, detect_agent_host
from .paired_targets import PairedTargetService
from .version import build_info


class HubInventory:
    """Read-only local inventory for the first Relmote Hub MVP.

    The Hub consumes credential-blind paired-target summaries. Live probes use
    the Agent Host's existing paired-target service but never return bearer
    credentials or stored endpoint URLs.
    """

    def __init__(
        self,
        *,
        paired_targets: PairedTargetService | None = None,
        host_factory: Callable[[], AgentHost] = detect_agent_host,
        build_factory: Callable[[], dict[str, str]] = build_info,
    ):
        self._paired_targets = paired_targets or PairedTargetService()
        self._host_factory = host_factory
        self._build_factory = build_factory

    @staticmethod
    def _live_error(exc: Exception) -> dict[str, Any]:
        if isinstance(exc, PermissionError):
            return {
                "reachable": True,
                "authority": "denied",
                "state": None,
                "detail": str(exc),
            }
        if isinstance(exc, ConnectionError):
            return {
                "reachable": False,
                "authority": "unknown",
                "state": None,
                "detail": str(exc),
            }
        return {
            "reachable": None,
            "authority": "unknown",
            "state": None,
            "detail": str(exc),
        }

    def snapshot(self, *, live: bool = False) -> dict[str, Any]:
        host = self._host_factory()
        build = self._build_factory()

        targets = []
        for target in self._paired_targets.targets():
            item = dict(target)
            item["role"] = "paired_target"
            if live:
                try:
                    status = self._paired_targets.status(str(item["name"]))
                except (
                    PermissionError,
                    ConnectionError,
                    KeyError,
                    ValueError,
                    OSError,
                ) as exc:
                    item["live"] = self._live_error(exc)
                else:
                    state = status.get("state")
                    item["live"] = {
                        "reachable": True,
                        "authority": "active" if state == "active" else "inactive",
                        "state": state,
                        "workspace": status.get("workspace"),
                        "capabilities": list(status.get("capabilities") or []),
                    }
            targets.append(item)

        return {
            "hub": {
                "role": "hub",
                "mode": "local-read-only",
                "co_located_agent_host": True,
                "authority": "inventory-only",
            },
            "agent_host": {
                "role": "agent_host",
                **host.as_dict(),
                "relmote": {
                    "display_version": build["display_version"],
                    "commit": build["commit"],
                    "short_commit": build["short_commit"],
                    "channel": build["channel"],
                },
            },
            "paired_targets": targets,
        }
