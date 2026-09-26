from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ToolEffect(str, Enum):
    READ_ONLY = "read-only"
    WORKSPACE_MUTATING = "workspace-mutating"


@dataclass(frozen=True)
class ToolRule:
    tool: str
    effect: ToolEffect
    allowed_subcommands: frozenset[str] = frozenset()


DEFAULT_TOOL_RULES = {
    "pytest": ToolRule("pytest", ToolEffect.READ_ONLY),
    "git-status": ToolRule("git-status", ToolEffect.READ_ONLY),
    "git-diff": ToolRule("git-diff", ToolEffect.READ_ONLY),
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
