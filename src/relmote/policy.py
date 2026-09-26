from __future__ import annotations

from .capabilities import KNOWN_CAPABILITIES
from .model import Action, Decision, Grant, Mode


def evaluate(action: Action, grant: Grant) -> Decision:
    """Evaluate an action against a bounded capability grant.

    Session state such as expiry, revocation, replay protection, and approval
    is enforced by the controller before transport dispatch.
    """

    unknown = [cap for cap in action.capabilities if cap not in KNOWN_CAPABILITIES]
    if unknown:
        return Decision(
            allowed=False,
            requires_approval=False,
            reason=f"unknown capabilities: {', '.join(unknown)}",
        )

    missing = [cap for cap in action.capabilities if cap not in grant.capabilities]
    if missing:
        return Decision(
            allowed=False,
            requires_approval=False,
            reason=f"missing capabilities: {', '.join(missing)}",
        )

    if grant.mode in {Mode.OBSERVE, Mode.TEACH}:
        return Decision(
            allowed=False,
            requires_approval=False,
            reason=f"{grant.mode.value} mode does not permit execution",
        )

    if grant.mode is Mode.ASSIST:
        return Decision(
            allowed=True,
            requires_approval=True,
            reason="assist mode requires explicit approval",
        )

    return Decision(
        allowed=True,
        requires_approval=False,
        reason="action fits active operate grant",
    )
