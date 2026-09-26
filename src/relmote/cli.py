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
from .webapp import serve_local
from .diagnostic_cli import status as diagnostic_status, diagnose as diagnostic_diagnose
from .ssh_target import SSHTarget
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

    ssh_parser = sub.add_parser(
        "ssh",
        help="work with an authorized external SSH target",
    )
    ssh_sub = ssh_parser.add_subparsers(dest="ssh_command", required=True)
    ssh_probes = ssh_sub.add_parser("probes", help="list available read-only probes")
    ssh_probes.set_defaults(
        func=lambda args: (print("\n".join(SSHTarget.available_probes())) or 0)
    )
    ssh_probe = ssh_sub.add_parser("probe", help="run one named read-only probe")
    ssh_probe.add_argument("target", help="SSH config host, Tailscale hostname/IP, or user@host")
    ssh_probe.add_argument("probe", choices=SSHTarget.available_probes())
    def run_ssh_probe(args):
        result = SSHTarget(args.target).run_probe(args.probe)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=__import__("sys").stderr)
        return 0 if result.ok else result.returncode or 1
    ssh_probe.set_defaults(func=run_ssh_probe)

    status_parser = sub.add_parser(
        "status",
        help="show read-only software-node status (useful locally or over SSH)",
    )
    status_parser.set_defaults(func=lambda args: diagnostic_status())

    diagnose_parser = sub.add_parser(
        "diagnose",
        help="run a read-only deterministic diagnosis",
    )
    diagnose_parser.add_argument("kind", choices=["network"])
    diagnose_parser.set_defaults(
        func=lambda args: diagnostic_diagnose(args.kind)
    )

    serve_parser = sub.add_parser(
        "serve",
        help="run the local-only software Relmote Agent and browser UI",
    )
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8787)
    serve_parser.add_argument(
        "--lan",
        action="store_true",
        help="explicit temporary read-only LAN preview with bearer token",
    )
    serve_parser.add_argument(
        "--lifetime-minutes",
        type=int,
        default=60,
        help="temporary LAN token lifetime",
    )
    serve_parser.set_defaults(
        func=lambda args: serve_local(
            host=args.host,
            port=args.port,
            lan=args.lan,
            lifetime_minutes=args.lifetime_minutes,
        )
    )

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
