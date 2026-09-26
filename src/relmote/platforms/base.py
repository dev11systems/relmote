from __future__ import annotations

from typing import Protocol


class PlatformAdapter(Protocol):
    def observations(self) -> dict[str, dict]: ...
