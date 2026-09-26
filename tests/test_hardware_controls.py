from relmote.hardware_controls import PhysicalControls
from relmote.safety import SafetyGate


class FakeGPIO:
    def __init__(self):
        self.values = {}
        self.outputs = {}

    def setup_input_pullup(self, pin):
        self.values.setdefault(pin, True)

    def setup_output(self, pin):
        self.outputs[pin] = False

    def read(self, pin):
        return self.values[pin]

    def write(self, pin, value):
        self.outputs[pin] = value


def press(controls, gpio, pin):
    gpio.values[pin] = False
    controls.poll()
    gpio.values[pin] = True
    controls.poll()


def test_authorize_arms_and_led_tracks_gate():
    now = [100.0]
    gpio = FakeGPIO()
    gate = SafetyGate(clock=lambda: now[0])
    controls = PhysicalControls(gpio, gate, clock=lambda: now[0])
    controls.setup()

    press(controls, gpio, controls.pins.authorize)

    assert gate.permits_output()
    assert gpio.outputs[controls.pins.armed_led]


def test_stop_latches_and_first_authorize_only_resets():
    now = [100.0]
    gpio = FakeGPIO()
    gate = SafetyGate(clock=lambda: now[0])
    controls = PhysicalControls(gpio, gate, clock=lambda: now[0])
    controls.setup()

    press(controls, gpio, controls.pins.authorize)
    now[0] += 1
    press(controls, gpio, controls.pins.stop)

    assert gate.snapshot().stop_latched
    assert not gate.permits_output()

    now[0] += 1
    press(controls, gpio, controls.pins.authorize)

    assert not gate.snapshot().stop_latched
    assert not gate.permits_output()

    now[0] += 1
    press(controls, gpio, controls.pins.authorize)
    assert gate.permits_output()


def test_activity_indicator_is_explicit():
    gpio = FakeGPIO()
    gate = SafetyGate()
    controls = PhysicalControls(gpio, gate)
    controls.setup()

    controls.set_activity(True)
    assert gpio.outputs[controls.pins.activity_led]
    controls.set_activity(False)
    assert not gpio.outputs[controls.pins.activity_led]
