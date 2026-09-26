from relmote.identity import (
    Pairing,
    PairingCode,
    Principal,
    PrincipalKind,
)


def test_pairing_code_has_human_fingerprint():
    code = PairingCode.generate("rm:test")
    chunks = code.fingerprint.split("-")

    assert len(chunks) == 4
    assert all(len(chunk) == 4 for chunk in chunks)


def test_pairing_requires_correct_principal_roles():
    node = Principal(PrincipalKind.NODE, "rm:test", "Pocket")
    controller = Principal(
        PrincipalKind.CONTROLLER,
        "rc:test",
        "Tablet",
    )

    pairing = Pairing(node, controller, "aaaa-bbbb-cccc-dddd")
    assert pairing.node.principal_id == "rm:test"
