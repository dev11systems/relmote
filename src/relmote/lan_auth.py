from __future__ import annotations

import secrets
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class TemporaryLANAccess:
    token: str
    expires_at_monotonic: float

    @classmethod
    def create(
        cls,
        *,
        lifetime_seconds: float = 3600,
        clock=time.monotonic,
    ) -> "TemporaryLANAccess":
        if lifetime_seconds <= 0:
            raise ValueError("lifetime_seconds must be positive")
        return cls(
            token=secrets.token_urlsafe(32),
            expires_at_monotonic=clock() + lifetime_seconds,
        )

    def valid(self, candidate: str | None, *, clock=time.monotonic) -> bool:
        if candidate is None or clock() >= self.expires_at_monotonic:
            return False
        return secrets.compare_digest(self.token, candidate)
