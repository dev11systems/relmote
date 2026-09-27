from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass


@dataclass
class PairingCode:
    digest: str
    session_id: str
    expires_at: float
    used: bool = False

    def active(self) -> bool:
        return not self.used and time.time() < self.expires_at


class PairingRegistry:
    def __init__(self):
        self._codes: dict[str, PairingCode] = {}

    @staticmethod
    def _digest(code: str) -> str:
        return hashlib.sha256(code.encode()).hexdigest()

    def create(self, session_id: str, *, lifetime_seconds: int = 300) -> str:
        # 8 decimal digits are convenient to type on phones/tablets while the
        # short lifetime + one-time exchange limits exposure.
        code = f"{secrets.randbelow(100_000_000):08d}"
        digest = self._digest(code)
        self._codes[digest] = PairingCode(
            digest=digest,
            session_id=session_id,
            expires_at=time.time() + lifetime_seconds,
        )
        return code

    def consume(self, code: str) -> str:
        record = self._codes.get(self._digest(code))
        if record is None or not record.active():
            raise PermissionError("pairing code is invalid, expired, or already used")
        record.used = True
        return record.session_id
