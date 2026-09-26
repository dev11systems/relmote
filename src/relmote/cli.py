from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import timedelta

from .audit import AuditLog
from .bench import run_bench
from .controller import RelmoteController
from .model import Action, Grant, Mode
from .session import Session, utcnow
from .transports.dry_run import DryRunTransport


def demo(args: argparse.Namespace) -> int:
    audit = AuditLog()
    controller = RelmoteController(DryRunTransport(), audit)

    grant = Grant(
        capabilities=frozenset({"input.keyboard"}),
        target_id=args.target,
        mode=Mode(args.mode),
        expires_at=utcnow() + timedelta(minutes=args.minutes),
    )
    session = Session(grant=grant, controller_id="local-cli")
    action = Action(
        kind="type_text",
        payload={"text": args.text},
        capabilities=("input.keyboard",),
    )

    decision = controller.propose(session, action)

    if args.approve:
        controller.approve(session, action.action_id)

    outcome = controller.execute(session, action)

    print(
        json.dumps(
            {
                "session_id": session.session_id,
                "action_id": action.action_id,
                "decision": asdict(decision),
                "outcome": asdict(outcome),
                "audit": [event.as_dict() for event in audit.events],
            },
            indent=2,
            default=str,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="relmote")
    sub = parser.add_subparsers(dest="command", required=True)

    demo_parser = sub.add_parser("demo", help="exercise the safe dry-run action loop")
    demo_parser.add_argument("--text", default="hello from Relmote")
    demo_parser.add_argument("--target", default="test-host")
    demo_parser.add_argument(
        "--mode",
        choices=[mode.value for mode in Mode],
        default=Mode.ASSIST.value,
    )
    demo_parser.add_argument("--minutes", type=int, default=5)
    demo_parser.add_argument(
        "--approve",
        action="store_true",
        help="explicitly approve the proposed action before execution",
    )
    demo_parser.set_defaults(func=demo)

    bench_parser = sub.add_parser(
        "bench",
        help="run the physical MVP-1 Pi/HID bench harness",
    )
    bench_parser.add_argument("--target", default="bench-target")
    bench_parser.add_argument("--minutes", type=int, default=15)
    bench_parser.add_argument("--key-delay", type=float, default=0.05)
    bench_parser.add_argument("--hid-device", default="/dev/hidg0")
    bench_parser.set_defaults(
        func=lambda args: run_bench(
            target_id=args.target,
            minutes=args.minutes,
            key_delay=args.key_delay,
            hid_device=args.hid_device,
        )
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
