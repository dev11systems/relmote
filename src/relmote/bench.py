from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from datetime import timedelta

from .controller import RelmoteController
from .gpio_backends import GpioZeroBackend
from .hardware_controls import PhysicalControls
from .model import Action, Grant, Mode
from .safety import SafetyGate
from .session import Session, utcnow
from .transports.linux_hid import LinuxHIDKeyboardTransport


@dataclass
class BenchRuntime:
    gate: SafetyGate
    controls: PhysicalControls
    controller: RelmoteController
    session: Session
    stop_event: threading.Event
    poll_thread: threading.Thread


def _poll_controls(controls: PhysicalControls, stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        controls.poll()
        time.sleep(0.01)


def create_runtime(
    *,
    target_id: str,
    minutes: int,
    key_delay: float,
    hid_device: str,
) -> BenchRuntime:
    gpio = GpioZeroBackend()
    gate = SafetyGate()
    controls = PhysicalControls(gpio, gate)
    controls.setup()

    transport = LinuxHIDKeyboardTransport(
        gate,
        device_path=hid_device,
        key_delay=key_delay,
        activity_changed=controls.set_activity,
    )
    controller = RelmoteController(transport)
    session = Session(
        controller_id="local-bench-controller",
        grant=Grant(
            capabilities=frozenset({"input.keyboard"}),
            target_id=target_id,
            mode=Mode.ASSIST,
            expires_at=utcnow() + timedelta(minutes=minutes),
        ),
    )
    stop_event = threading.Event()
    poll_thread = threading.Thread(
        target=_poll_controls,
        args=(controls, stop_event),
        name="relmote-gpio",
        daemon=True,
    )
    poll_thread.start()
    return BenchRuntime(gate, controls, controller, session, stop_event, poll_thread)


def run_bench(
    *,
    target_id: str = "bench-target",
    minutes: int = 15,
    key_delay: float = 0.05,
    hid_device: str = "/dev/hidg0",
) -> int:
    runtime = create_runtime(
        target_id=target_id,
        minutes=minutes,
        key_delay=key_delay,
        hid_device=hid_device,
    )

    print("RELMOTE MVP-1 BENCH")
    print(f"target: {target_id}")
    print("mode: ASSIST")
    print("type :quit to exit")
    print("physical AUTHORIZE is required before every output lease")
    print()

    try:
        while runtime.session.is_active():
            snapshot = runtime.gate.snapshot()
            state = "STOP-LATCHED" if snapshot.stop_latched else (
                f"ARMED {snapshot.seconds_remaining:.1f}s" if snapshot.armed else "DISARMED"
            )
            print(f"safety: {state}")
            text = input("text> ")
            if text == ":quit":
                break
            if not text:
                continue

            action = Action(
                kind="type_text",
                payload={"text": text},
                capabilities=("input.keyboard",),
            )
            decision = runtime.controller.propose(runtime.session, action)
            print(f"proposal: {len(text)} chars / {decision.reason}")
            if not decision.allowed:
                print("DENIED")
                continue

            approval = input("approve this exact action? [y/N] ").strip().lower()
            if approval not in {"y", "yes"}:
                print("rejected")
                continue

            runtime.controller.approve(runtime.session, action.action_id)

            if not runtime.gate.permits_output():
                print("waiting for physical AUTHORIZE...")
                while runtime.session.is_active() and not runtime.gate.permits_output():
                    if runtime.gate.snapshot().stop_latched:
                        print("STOP is latched; press AUTHORIZE once to reset, again to arm.")
                    time.sleep(0.25)

            if not runtime.session.is_active():
                print("session expired/revoked")
                break

            outcome = runtime.controller.execute(runtime.session, action)
            result = outcome.result or {}
            print(
                f"sent {result.get('characters_sent', 0)}/"
                f"{result.get('characters_requested', len(text))}"
            )
            if result.get("interrupted"):
                print(f"INTERRUPTED by {result.get('stopped_by')}")
            elif result.get("completed"):
                print("complete")
            elif result.get("error"):
                print(f"transport error: {result['error']}")
            print()

    except KeyboardInterrupt:
        print("\nrevoking bench session")
    finally:
        runtime.controller.revoke(runtime.session)
        runtime.gate.latch_stop()
        runtime.controls.set_activity(False)
        runtime.stop_event.set()
        runtime.poll_thread.join(timeout=1)

    return 0
