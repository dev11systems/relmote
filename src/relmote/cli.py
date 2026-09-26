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
from .ssh_workspace import SSHWorkspace
from .workspace import WorkspacePolicy
from .app import run_app
from .version import build_info
from .updater import update_repo_preview
from .doctor import print_doctor
from .check_cli import run_check
from .help import print_help_topic, topic_names
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
    sub = parser.add_subparsers(dest="command", required=False)

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

    help_parser = sub.add_parser(
        "help",
        help="plain-language help and workflow guides",
    )
    help_parser.add_argument(
        "topic",
        nargs="?",
        choices=(*topic_names(), "topics"),
    )
    def run_help(args):
        if args.topic == "topics":
            print("\n".join(topic_names()))
            return 0
        return print_help_topic(args.topic)
    help_parser.set_defaults(func=run_help)

    check_parser = sub.add_parser(
        "check",
        help="run the plain-language full system check",
    )
    check_parser.add_argument(
        "--json",
        action="store_true",
        help="emit structured findings and observations",
    )
    check_parser.set_defaults(func=lambda args: run_check(as_json=args.json))

    doctor_parser = sub.add_parser(
        "doctor",
        help="check whether this machine is ready for the Relmote preview",
    )
    doctor_parser.set_defaults(func=lambda args: print_doctor())

    update_parser = sub.add_parser(
        "update",
        help="update a repository-installed Relmote development preview",
    )
    update_parser.add_argument(
        "--check",
        action="store_true",
        help="show the preview update action without changing anything",
    )
    update_parser.set_defaults(
        func=lambda args: update_repo_preview(dry_run=args.check)
    )

    version_parser = sub.add_parser(
        "version",
        help="show Relmote version/build information",
    )
    version_parser.add_argument(
        "--full",
        action="store_true",
        help="show the full source commit identifier",
    )
    def run_version(args):
        info = build_info()
        build = info["commit"] if args.full else info["short_commit"]
        print(f'Relmote {info["version"]}')
        print(f'Channel: {info["channel"]}')
        print(f'Build: {build}')
        return 0
    version_parser.set_defaults(func=run_version)

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

    workspace_parser = sub.add_parser(
        "workspace",
        help="operate inside one explicitly configured remote SSH workspace",
    )
    workspace_parser.add_argument("target")
    workspace_parser.add_argument("root", help="absolute remote workspace root")
    workspace_sub = workspace_parser.add_subparsers(dest="workspace_command", required=True)

    workspace_list = workspace_sub.add_parser("list")
    workspace_list.add_argument("path", nargs="?", default=".")
    workspace_read = workspace_sub.add_parser("read")
    workspace_read.add_argument("path")
    workspace_sub.add_parser("git-status")
    workspace_sub.add_parser("git-diff")

    def run_workspace(args):
        ws = SSHWorkspace(args.target, WorkspacePolicy.create(args.root))
        if args.workspace_command == "list":
            result = ws.list(args.path)
        elif args.workspace_command == "read":
            result = ws.read(args.path)
        elif args.workspace_command == "git-status":
            result = ws.git_status()
        elif args.workspace_command == "git-diff":
            result = ws.git_diff()
        else:
            raise ValueError("unknown workspace command")
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=__import__("sys").stderr)
        return 0 if result.ok else result.returncode or 1

    for workspace_command_parser in (workspace_list, workspace_read):
        workspace_command_parser.set_defaults(func=run_workspace)
    workspace_sub.choices["git-status"].set_defaults(func=run_workspace)
    workspace_sub.choices["git-diff"].set_defaults(func=run_workspace)

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
    if args.command is None:
        return run_app()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
