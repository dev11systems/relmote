from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .agent import AgentObservation, LocalAgent
from .diagnostics import DiagnosticFinding, diagnose_network
from pathlib import Path


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class SoftwareNodeIdentity:
    node_id: str
    display_name: str
    fingerprint: str

    @classmethod
    def ephemeral(cls, display_name: str) -> "SoftwareNodeIdentity":
        raw = secrets.token_hex(16)
        grouped = "-".join(raw[i:i+4] for i in range(0, 16, 4)).upper()
        return cls(
            node_id=f"rm:ephemeral:{raw}",
            display_name=display_name,
            fingerprint=grouped,
        )


@dataclass
class ObserveSession:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=utcnow_iso)
    revoked: bool = False

    def revoke(self) -> None:
        self.revoked = True


@dataclass(frozen=True)
class DiagnosticTask:
    task_id: str
    task_type: str
    created_at: str
    observations: tuple[AgentObservation, ...]
    findings: tuple[DiagnosticFinding, ...] = ()


class SoftwareNode:
    """S2 in-process software Relmote node."""

    TASKS = {
        "system-overview": (
            "system.identify",
            "system.platform",
            "system.memory",
            "storage.inspect",
        ),
        "network-overview": (
            "system.identify",
            "network.inspect",
        ),
        "storage-overview": (
            "storage.inspect",
        ),
    }

    def __init__(self, agent: LocalAgent | None = None) -> None:
        self.agent = agent or LocalAgent()
        self.identity = SoftwareNodeIdentity.ephemeral(
            self.agent.observe("system.identify").data["hostname"]
        )
        self.session: ObserveSession | None = None
        self.tasks: list[DiagnosticTask] = []

    def start_observe_session(self) -> ObserveSession:
        if self.session and not self.session.revoked:
            return self.session
        self.session = ObserveSession()
        return self.session

    def revoke_session(self) -> None:
        if self.session:
            self.session.revoke()

    def run_task(self, task_type: str) -> DiagnosticTask:
        if not self.session or self.session.revoked:
            raise PermissionError("an active Observe session is required")
        if task_type == "diagnose-network":
            report = diagnose_network(self.agent)
            task = DiagnosticTask(
                task_id=str(uuid4()),
                task_type=task_type,
                created_at=utcnow_iso(),
                observations=report.observations,
                findings=report.findings,
            )
        else:
            capabilities = self.TASKS.get(task_type)
            if capabilities is None:
                raise ValueError(f"unknown diagnostic task: {task_type}")
            task = DiagnosticTask(
                task_id=str(uuid4()),
                task_type=task_type,
                created_at=utcnow_iso(),
                observations=tuple(self.agent.observe(cap) for cap in capabilities),
            )
        self.tasks.append(task)
        return task

    def self_check(self) -> dict:
        checks = {
            "observe_session": bool(self.session and not self.session.revoked),
            "capability_count": len(self.agent.capabilities),
            "python_runtime": self.agent.observe("system.platform").data.get("python"),
            "hostname_available": bool(
                self.agent.observe("system.identify").data.get("hostname")
            ),
            "storage_observation": (
                self.agent.observe("storage.inspect").data.get("total_bytes", 0) > 0
            ),
        }
        return {
            "status": "ok" if all(
                value for key, value in checks.items()
                if key != "observe_session"
            ) else "attention",
            "checks": checks,
            "note": "Observe session is expected to be false before the user starts one.",
        }

    def snapshot(self) -> dict:
        session = None
        if self.session:
            session = {
                "session_id": self.session.session_id,
                "started_at": self.session.started_at,
                "mode": "observe",
                "revoked": self.session.revoked,
            }
        return {
            "node": {
                "node_id": self.identity.node_id,
                "name": self.identity.display_name,
                "fingerprint": self.identity.fingerprint,
                "implementation": "software-ephemeral",
            },
            "target": {
                "target_id": "target:self",
                "name": self.identity.display_name,
                "relationship": "same-host",
            },
            "capabilities": sorted(self.agent.capabilities),
            "session": session,
            "tasks": [
                {
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "created_at": task.created_at,
                    "findings": [
                        {
                            "status": finding.status,
                            "statement": finding.statement,
                            "evidence": list(finding.evidence),
                            "uncertainty": finding.uncertainty,
                        }
                        for finding in task.findings
                    ],
                    "observations": [
                        {"capability": obs.capability, "data": obs.data}
                        for obs in task.observations
                    ],
                }
                for task in self.tasks[-20:]
            ],
        }
