from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from .tool_policy import ToolEffect, classify_tool


class ToolActionState(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    EXECUTED = "executed"
    REJECTED = "rejected"


@dataclass
class ToolAction:
    tool: str
    args: tuple[str, ...]
    effect: ToolEffect
    action_id: str = field(default_factory=lambda: str(uuid4()))
    state: ToolActionState = ToolActionState.PROPOSED

    @classmethod
    def create(cls, tool: str, args: tuple[str, ...] = ()) -> "ToolAction":
        return cls(tool=tool, args=args, effect=classify_tool(tool, args))

    @property
    def requires_approval(self) -> bool:
        return self.effect in {ToolEffect.WORKSPACE_EXECUTION, ToolEffect.WORKSPACE_MUTATING, ToolEffect.SYSTEM_MUTATING}

    def approve(self) -> None:
        if self.state is not ToolActionState.PROPOSED:
            raise ValueError("tool action is not proposed")
        self.state = ToolActionState.APPROVED

    def reject(self) -> None:
        if self.state is not ToolActionState.PROPOSED:
            raise ValueError("tool action is not proposed")
        self.state = ToolActionState.REJECTED

    def mark_executed(self) -> None:
        if self.requires_approval and self.state is not ToolActionState.APPROVED:
            raise PermissionError("mutating tool action requires approval")
        if not self.requires_approval and self.state is not ToolActionState.PROPOSED:
            raise ValueError("read-only action has invalid state")
        self.state = ToolActionState.EXECUTED
