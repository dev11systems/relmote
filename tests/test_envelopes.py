import pytest

from relmote.envelopes import Deduplicator, Envelope, EnvelopeKind


def test_envelope_priority_is_bounded():
    with pytest.raises(ValueError):
        Envelope(EnvelopeKind.TASK, {}, priority=101)


def test_delivery_deduplicator():
    seen = Deduplicator(max_ids=2)

    assert seen.first_seen("a")
    assert not seen.first_seen("a")
    assert seen.first_seen("b")
    assert seen.first_seen("c")

    # Old IDs can eventually fall out of the bounded delivery cache. Target
    # action replay protection remains a separate lower-layer mechanism.
    assert seen.first_seen("a")
