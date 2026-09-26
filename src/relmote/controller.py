from __future__ import annotations

from .audit import AuditLog
from .model import Action, Decision, ExecutionOutcome
from .policy import evaluate
from .session import Session
from .transports.base import Transport


class RelmoteController:
    """Mandatory policy boundary between proposed actions and a transport."""

    def __init__(self, transport: Transport, audit: AuditLog | None = None) -> None:
        self.transport = transport
        self.audit = audit or AuditLog()

    def _session_block(self, session: Session, action: Action) -> ExecutionOutcome | None:
        if session.revoked_at is not None:
            return ExecutionOutcome(False, "denied", "session revoked")

        if session.is_expired():
            return ExecutionOutcome(False, "denied", "session expired")

        if session.was_executed(action.action_id):
            return ExecutionOutcome(False, "denied", "action already executed")

        return None

    def propose(self, session: Session, action: Action) -> Decision:
        self.audit.append(
            "action.proposed",
            session.session_id,
            action_id=action.action_id,
            details={
                "kind": action.kind,
                "capabilities": list(action.capabilities),
                "target_id": session.grant.target_id,
            },
        )

        blocked = self._session_block(session, action)
        if blocked is not None:
            decision = Decision(False, False, blocked.reason)
        else:
            decision = evaluate(action, session.grant)

        self.audit.append(
            "policy.decision",
            session.session_id,
            action_id=action.action_id,
            details={
                "allowed": decision.allowed,
                "requires_approval": decision.requires_approval,
                "reason": decision.reason,
            },
        )
        return decision

    def approve(self, session: Session, action_id: str) -> bool:
        if not session.is_active():
            return False
        if session.was_executed(action_id):
            return False

        session.approve(action_id)
        self.audit.append(
            "action.approved",
            session.session_id,
            action_id=action_id,
        )
        return True

    def revoke(self, session: Session) -> None:
        session.revoke()
        self.audit.append("session.revoked", session.session_id)

    def execute(self, session: Session, action: Action) -> ExecutionOutcome:
        blocked = self._session_block(session, action)
        if blocked is not None:
            self.audit.append(
                "action.denied",
                session.session_id,
                action_id=action.action_id,
                details={"reason": blocked.reason},
            )
            return blocked

        decision = evaluate(action, session.grant)
        if not decision.allowed:
            outcome = ExecutionOutcome(False, "denied", decision.reason)
            self.audit.append(
                "action.denied",
                session.session_id,
                action_id=action.action_id,
                details={"reason": decision.reason},
            )
            return outcome

        if decision.requires_approval and not session.is_approved(action.action_id):
            outcome = ExecutionOutcome(False, "approval_required", decision.reason)
            self.audit.append(
                "action.waiting_approval",
                session.session_id,
                action_id=action.action_id,
            )
            return outcome

        result = self.transport.execute(action)
        session.mark_executed(action.action_id)

        self.audit.append(
            "action.executed",
            session.session_id,
            action_id=action.action_id,
            details={
                "kind": action.kind,
                "transport": self.transport.capabilities.name,
                "target_id": session.grant.target_id,
            },
        )

        return ExecutionOutcome(
            True,
            "executed",
            "action dispatched through authorized transport",
            result,
        )
