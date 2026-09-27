from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock, Thread
from uuid import uuid4
import secrets

from .software_node import SoftwareNode
from .access_policy import AccessPolicy
from .feature_status import remote_feature_status
from .terminal import TerminalAuthority, TerminalSession, TerminalState
from .terminal_manager import TerminalManager
from .screen_session import ScreenSession
from .portal_dbus import request_monitor_share
from .agent_bridge import AgentGrant, create_grant


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RuntimeEvent:
    event_id: str
    kind: str
    created_at: str
    data: dict


@dataclass
class RelmoteRuntime:
    """Authoritative in-process state shared by all frontends."""

    node: SoftwareNode = field(default_factory=SoftwareNode)
    support_access: AccessPolicy = field(default_factory=AccessPolicy)
    terminal_sessions: dict[str, TerminalSession] = field(default_factory=dict)
    terminal_manager: TerminalManager = field(default_factory=TerminalManager)
    screen_sessions: dict[str, ScreenSession] = field(default_factory=dict)
    agent_grants: dict[str, AgentGrant] = field(default_factory=dict)
    _events: list[RuntimeEvent] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock)

    def emit(self, kind: str, data: dict | None = None) -> RuntimeEvent:
        event = RuntimeEvent(
            event_id=str(uuid4()),
            kind=kind,
            created_at=utcnow_iso(),
            data=data or {},
        )
        with self._lock:
            self._events.append(event)
            self._events = self._events[-200:]
        return event

    def start_checks(self) -> dict:
        with self._lock:
            session = self.node.start_observe_session()
            self.emit("session.started", {
                "session_id": session.session_id,
                "mode": "observe",
            })
            return self.snapshot()

    def stop_checks(self) -> dict:
        with self._lock:
            self.node.revoke_session()
            self.emit("session.revoked")
            return self.snapshot()

    def enable_support_until_disabled(self) -> dict:
        with self._lock:
            self.support_access.enable_until_disabled()
            self.emit("support.enabled", {"mode": "until-disabled"})
            return self.snapshot()

    def enable_support_for(self, seconds: float) -> dict:
        with self._lock:
            self.support_access.enable_for(seconds)
            self.emit("support.enabled", {"mode": "timed", "seconds": seconds})
            return self.snapshot()

    def disable_support(self) -> dict:
        with self._lock:
            self.support_access.disable()
            self.node.revoke_session()
            self.terminal_manager.close_all()
            for terminal in self.terminal_sessions.values():
                terminal.revoke()
            for screen in self.screen_sessions.values():
                screen.revoke()
            for grant in self.agent_grants.values():
                grant.session.revoke()
            self.emit("support.disabled")
            return self.snapshot()


    def request_agent(
        self,
        root: str,
        capabilities: list[str],
        *,
        controller: str = "external-agent",
    ) -> AgentGrant:
        with self._lock:
            if not self.support_access.available():
                raise PermissionError("remote support is off")
            grant = create_grant(
                root,
                controller=controller,
                capabilities=capabilities,
            )
            self.agent_grants[grant.session.session_id] = grant
            self.emit("agent.requested", {
                "agent_session_id": grant.session.session_id,
                "controller": controller,
                "workspace": root,
                "capabilities": capabilities,
            })
            return grant

    def approve_agent(self, session_id: str) -> AgentGrant:
        with self._lock:
            grant = self.agent_grants[session_id]
            grant.session.approve()
            self.emit("agent.approved", {"agent_session_id": session_id})
            return grant

    def revoke_agent(self, session_id: str) -> AgentGrant:
        with self._lock:
            grant = self.agent_grants[session_id]
            grant.session.revoke()
            self.emit("agent.revoked", {"agent_session_id": session_id})
            return grant

    def agent_by_token(self, token: str) -> AgentGrant:
        with self._lock:
            for grant in self.agent_grants.values():
                if secrets.compare_digest(grant.token, token):
                    if grant.session.state.value != "active":
                        raise PermissionError("agent session is not active")
                    return grant
        raise PermissionError("invalid agent session token")

    def request_screen(self, *, controller: str = "remote-controller") -> ScreenSession:
        with self._lock:
            if not self.support_access.available():
                raise PermissionError("remote support is off")
            screen = remote_feature_status().get("screen", {})
            if screen.get("session_type") != "wayland":
                raise RuntimeError("screen observe preview currently requires Wayland")
            if not screen.get("portal_ready"):
                raise RuntimeError(
                    screen.get("portal_note") or "Wayland ScreenCast portal is unavailable"
                )
            session = ScreenSession(controller=controller)
            self.screen_sessions[session.session_id] = session
            self.emit("screen.requested", {
                "screen_session_id": session.session_id,
                "controller": controller,
                "authority": session.authority.value,
            })
            return session

    def approve_screen(self, session_id: str) -> ScreenSession:
        with self._lock:
            session = self.screen_sessions[session_id]
            session.approve()
            session.awaiting_os_consent()
            self.emit("screen.approved", {
                "screen_session_id": session_id,
                "next": "os-consent",
            })
            Thread(
                target=self._run_screen_portal,
                args=(session_id,),
                daemon=True,
                name=f"relmote-screen-{session_id[:8]}",
            ).start()
            return session

    def _run_screen_portal(self, session_id: str) -> None:
        try:
            response = request_monitor_share()
            with self._lock:
                session = self.screen_sessions.get(session_id)
                if session is None or session.state.value != "os-consent":
                    return
                session.activate()
                self.emit("screen.portal-approved", {
                    "screen_session_id": session_id,
                    "portal_response": response.results_text,
                })
        except Exception as exc:
            with self._lock:
                session = self.screen_sessions.get(session_id)
                if session is None or session.state.value == "ended":
                    return
                session.fail(f"{type(exc).__name__}: {exc}")
                self.emit("screen.failed", {
                    "screen_session_id": session_id,
                    "error": session.error,
                })

    def deny_screen(self, session_id: str) -> ScreenSession:
        with self._lock:
            session = self.screen_sessions[session_id]
            session.revoke()
            self.emit("screen.denied", {"screen_session_id": session_id})
            return session

    def end_screen(self, session_id: str) -> ScreenSession:
        with self._lock:
            session = self.screen_sessions[session_id]
            session.revoke()
            self.emit("screen.ended", {"screen_session_id": session_id})
            return session

    def request_terminal(
        self,
        target: str,
        *,
        controller: str = "remote-controller",
        authority: TerminalAuthority = TerminalAuthority.USER,
    ) -> TerminalSession:
        with self._lock:
            if not self.support_access.available():
                raise PermissionError("remote support is off")
            session = TerminalSession(
                target=target,
                authority=authority,
                controller=controller,
            )
            self.terminal_sessions[session.session_id] = session
            self.emit("terminal.requested", {
                "terminal_session_id": session.session_id,
                "target": target,
                "controller": controller,
                "authority": authority.value,
            })
            return session

    def approve_terminal(self, session_id: str) -> TerminalSession:
        with self._lock:
            session = self.terminal_sessions[session_id]
            if session.target == "this-computer":
                # Attach transactionally: do not leave the permission model
                # claiming ACTIVE if the PTY/shell failed to start.
                session.approve()
                try:
                    self.terminal_manager.attach(session)
                except Exception:
                    session.revoke()
                    self.emit("terminal.failed", {
                        "terminal_session_id": session_id,
                    })
                    raise
            else:
                session.approve()
            self.emit("terminal.approved", {
                "terminal_session_id": session_id,
            })
            return session

    def deny_terminal(self, session_id: str) -> TerminalSession:
        with self._lock:
            session = self.terminal_sessions[session_id]
            session.deny()
            self.emit("terminal.denied", {
                "terminal_session_id": session_id,
            })
            return session

    def end_terminal(self, session_id: str) -> TerminalSession:
        with self._lock:
            session = self.terminal_sessions[session_id]
            self.terminal_manager.close(session_id)
            if session.state is TerminalState.ACTIVE:
                session.end()
            self.emit("terminal.ended", {
                "terminal_session_id": session_id,
            })
            return session

    def read_terminal(self, session_id: str) -> bytes:
        with self._lock:
            session = self.terminal_sessions[session_id]
            if session.state is not TerminalState.ACTIVE:
                raise PermissionError("terminal session is not active")
            return self.terminal_manager.read(session_id)

    def write_terminal(self, session_id: str, data: bytes) -> None:
        with self._lock:
            session = self.terminal_sessions[session_id]
            if session.state is not TerminalState.ACTIVE:
                raise PermissionError("terminal session is not active")
            self.terminal_manager.write(session_id, data)

    def run_task(self, task_type: str) -> dict:
        with self._lock:
            task = self.node.run_task(task_type)
            self.emit("task.completed", {
                "task_id": task.task_id,
                "task_type": task.task_type,
            })
            return self.snapshot()

    def events_since(self, offset: int = 0) -> dict:
        with self._lock:
            events = self._events[offset:]
            return {
                "offset": offset + len(events),
                "events": [
                    {
                        "event_id": event.event_id,
                        "kind": event.kind,
                        "created_at": event.created_at,
                        "data": event.data,
                    }
                    for event in events
                ],
            }

    def snapshot(self) -> dict:
        with self._lock:
            value = self.node.snapshot()
            value["runtime"] = {
                "event_count": len(self._events),
                "frontends": ["cli", "tui-preview", "web"],
            }
            value["support"] = {
                "available": self.support_access.available(),
                "mode": self.support_access.mode.value,
            }
            value["features"] = remote_feature_status()
            value["agent_sessions"] = [
                grant.public() for grant in self.agent_grants.values()
            ]
            value["screen_sessions"] = [
                {
                    "session_id": session.session_id,
                    "controller": session.controller,
                    "authority": session.authority.value,
                    "state": session.state.value,
                    "error": session.error,
                }
                for session in self.screen_sessions.values()
            ]
            value["terminal_sessions"] = [
                {
                    "session_id": session.session_id,
                    "target": session.target,
                    "controller": session.controller,
                    "authority": session.authority.value,
                    "state": session.state.value,
                }
                for session in self.terminal_sessions.values()
            ]
            return value
