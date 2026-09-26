from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ToolEffect(str, Enum):
    OBSERVATION = "observation"
    WORKSPACE_EXECUTION = "workspace-execution"
    WORKSPACE_MUTATING = "workspace-mutating"
    SYSTEM_MUTATING = "system-mutating"


@dataclass(frozen=True)
class ToolRule:
    tool: str
    effect: ToolEffect
    allowed_subcommands: frozenset[str] = frozenset()


DEFAULT_TOOL_RULES = {
    "git-status": ToolRule("git-status", ToolEffect.OBSERVATION),
    "git-diff": ToolRule("git-diff", ToolEffect.OBSERVATION),
    # Tests/build tools may have side effects inside a workspace and may use
    # network/resources. They are not described as read-only.
    "pytest": ToolRule("pytest", ToolEffect.WORKSPACE_EXECUTION),
    "git": ToolRule(
        "git",
        ToolEffect.WORKSPACE_MUTATING,
        frozenset({"add", "restore"}),
    ),
}


def classify_tool(tool: str, args: tuple[str, ...]) -> ToolEffect:
    rule = DEFAULT_TOOL_RULES.get(tool)
    if rule is None:
        raise PermissionError(f"tool is not in Relmote preview policy: {tool}")

    if rule.allowed_subcommands:
        if not args or args[0] not in rule.allowed_subcommands:
            raise PermissionError(
                f"subcommand is not allowed for {tool}: "
                f"{args[0] if args else '<none>'}"
            )

    return rule.effect
