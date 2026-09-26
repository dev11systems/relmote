from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PowerLoad:
    name: str
    typical_mw: int
    peak_mw: int

    def __post_init__(self) -> None:
        if self.typical_mw < 0 or self.peak_mw < 0:
            raise ValueError("power values must be non-negative")
        if self.peak_mw < self.typical_mw:
            raise ValueError("peak_mw must be >= typical_mw")


@dataclass(frozen=True)
class PowerBudget:
    available_mw: int
    reserve_mw: int = 0

    def __post_init__(self) -> None:
        if self.available_mw < 0 or self.reserve_mw < 0:
            raise ValueError("budget values must be non-negative")
        if self.reserve_mw > self.available_mw:
            raise ValueError("reserve cannot exceed available power")

    @property
    def usable_mw(self) -> int:
        return self.available_mw - self.reserve_mw

    def admit(self, loads: list[PowerLoad], *, use_peak: bool = True) -> bool:
        demand = sum(
            load.peak_mw if use_peak else load.typical_mw
            for load in loads
        )
        return demand <= self.usable_mw

    def remaining_mw(self, loads: list[PowerLoad], *, use_peak: bool = True) -> int:
        demand = sum(
            load.peak_mw if use_peak else load.typical_mw
            for load in loads
        )
        return self.usable_mw - demand


def ideal_runtime_hours(capacity_wh: float, average_w: float) -> float:
    """Idealized runtime before conversion losses/reserve margins."""
    if capacity_wh <= 0:
        raise ValueError("capacity_wh must be positive")
    if average_w <= 0:
        raise ValueError("average_w must be positive")
    return capacity_wh / average_w
