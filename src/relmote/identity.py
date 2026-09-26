from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from enum import Enum


class PrincipalKind(str, Enum):
    CONTROLLER = "controller"
    NODE = "node"


@dataclass(frozen=True)
class Principal:
    """Public identity reference.

    This model deliberately does not define production key storage or crypto.
    """

    kind: PrincipalKind
    principal_id: str
    display_name: str


@dataclass(frozen=True)
class PairingCode:
    node_id: str
    secret: str

    @classmethod
    def generate(cls, node_id: str) -> "PairingCode":
        # Prototype-only pairing material. Production pairing must use a
        # reviewed authenticated key-agreement protocol.
        return cls(node_id=node_id, secret=secrets.token_urlsafe(18))

    @property
    def fingerprint(self) -> str:
        digest = hashlib.sha256(self.secret.encode()).hexdigest()
        return "-".join(digest[i : i + 4] for i in range(0, 16, 4))


@dataclass(frozen=True)
class Pairing:
    node: Principal
    controller: Principal
    pairing_fingerprint: str

    def __post_init__(self) -> None:
        if self.node.kind is not PrincipalKind.NODE:
            raise ValueError("node principal must have NODE kind")
        if self.controller.kind is not PrincipalKind.CONTROLLER:
            raise ValueError("controller principal must have CONTROLLER kind")
