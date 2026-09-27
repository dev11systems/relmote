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

    @staticmethod
    def _reconcile_live(live: dict[str, Any]) -> dict[str, Any]:
        reachable = live.get("reachable")
        authority = live.get("authority")
        state = live.get("state")
        detail = str(live.get("detail") or "")
        lowered = detail.lower()

        if reachable is False:
            return {
                "health": "unreachable",
                "needs_attention": True,
                "recommended_action": "check private transport and target availability",
            }
        if authority == "active" and state == "active":
            return {
                "health": "active",
                "needs_attention": False,
                "recommended_action": None,
            }
        if authority == "denied":
            if "invalid agent session token" in lowered:
                health = "stale_credential"
                action = "create a new Target grant and re-pair this profile"
            elif "session is not active" in lowered:
                health = "revoked"
                action = "create a new Target grant and re-pair if access is still needed"
            else:
                health = "denied"
                action = "review the Target grant before re-pairing"
            return {
                "health": health,
                "needs_attention": True,
                "recommended_action": action,
            }
        if state and state != "active":
            return {
                "health": "inactive",
                "needs_attention": True,
                "recommended_action": "review or replace the inactive Target grant",
            }
        return {
            "health": "unknown",
            "needs_attention": True,
            "recommended_action": "review live Target status",
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
                item["current"] = self._reconcile_live(item["live"])
            targets.append(item)

        summary = {
            "total": len(targets),
            "active": 0,
            "attention": 0,
            "unreachable": 0,
            "revoked": 0,
            "stale_credential": 0,
        }
        if live:
            for item in targets:
                current = item.get("current") or {}
                health = current.get("health")
                if current.get("needs_attention"):
                    summary["attention"] += 1
                if health in summary:
                    summary[health] += 1

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
            "summary": summary,
        }
