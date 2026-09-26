from __future__ import annotations

from dataclasses import dataclass

from .topology import Feedback, TargetPath


@dataclass(frozen=True)
class TaskRequirements:
    needs_input: bool = False
    needs_text_feedback: bool = False
    needs_screen_feedback: bool = False
    needs_preboot: bool = False
    prefer_native: bool = True


@dataclass(frozen=True)
class RouteDecision:
    path: TargetPath | None
    usable: bool
    reason: str
    limitations: tuple[str, ...] = ()


def select_system_path(
    paths: tuple[TargetPath, ...],
    requirements: TaskRequirements,
) -> RouteDecision:
    """Select the least-invasive useful target path.

    This is intentionally simple and deterministic. It does not grant
    authorization; it only evaluates technical suitability.
    """

    candidates: list[tuple[int, TargetPath, tuple[str, ...]]] = []

    for path in paths:
        limitations: list[str] = []

        if requirements.needs_preboot and not path.works_before_os:
            continue

        if requirements.needs_text_feedback:
            if path.feedback not in {Feedback.TEXT, Feedback.STRUCTURED}:
                continue

        if requirements.needs_screen_feedback:
            if path.feedback is not Feedback.SCREEN:
                continue

        if requirements.needs_input and path.transport.startswith("observe."):
            continue

        score = 0

        # Prefer native structured/text paths over emulated human input when
        # they satisfy the same task.
        if requirements.prefer_native and path.native:
            score += 100

        if path.feedback is Feedback.STRUCTURED:
            score += 40
        elif path.feedback is Feedback.TEXT:
            score += 30
        elif path.feedback is Feedback.SCREEN:
            score += 20
        else:
            limitations.append("no target feedback")

        if path.bidirectional:
            score += 10

        if path.works_before_os:
            score += 2

        candidates.append((score, path, tuple(limitations)))

    if not candidates:
        return RouteDecision(
            path=None,
            usable=False,
            reason="no system path satisfies task requirements",
        )

    candidates.sort(key=lambda item: (item[0], item[1].path_id), reverse=True)
    _, selected, limitations = candidates[0]

    return RouteDecision(
        path=selected,
        usable=True,
        reason=f"selected {selected.transport}",
        limitations=limitations,
    )
