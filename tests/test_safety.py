from relmote.safety import SafetyGate


def test_gate_starts_disarmed():
    now = [100.0]
    gate = SafetyGate(clock=lambda: now[0])

    assert not gate.permits_output()
    assert gate.stop_requested()


def test_arm_is_time_bounded():
    now = [100.0]
    gate = SafetyGate(clock=lambda: now[0])

    assert gate.arm_for(5)
    assert gate.permits_output()

    now[0] = 105.0
    assert not gate.permits_output()


def test_stop_latches_and_cannot_be_rearmed_until_reset():
    now = [100.0]
    gate = SafetyGate(clock=lambda: now[0])

    assert gate.arm_for(30)
    gate.latch_stop()

    assert not gate.permits_output()
    assert gate.snapshot().stop_latched
    assert not gate.arm_for(30)

    gate.reset_stop()
    assert not gate.permits_output()
    assert gate.arm_for(30)
    assert gate.permits_output()


def test_reset_never_rearms_implicitly():
    now = [100.0]
    gate = SafetyGate(clock=lambda: now[0])

    gate.arm_for(30)
    gate.latch_stop()
    gate.reset_stop()

    assert not gate.permits_output()
