from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import timedelta

from .audit import AuditLog
from .debug_log import configure_logging, log_path, tail_log
from .bench import run_bench
from .controller import RelmoteController
from .model import Action, Grant, Mode
from .session import Session, utcnow
from .webapp import serve_local
from .diagnostic_cli import status as diagnostic_status, diagnose as diagnostic_diagnose
from .ssh_target import SSHTarget
from .ssh_workspace import SSHWorkspace
from .workspace import WorkspacePolicy
from .agent_transport import tailscale_transport
from .agent_access import enable_private_transport, disable_private_transport, serve_status
from .agent_scope import classify_scope
from .agent_client import RelmoteAgentClient, pair as pair_agent
from .agent_profiles import save_profile
from .agent_host import detect_agent_host
from .paired_targets import PairedTargetService
from .app import run_app
from .version import build_info
from .updater import update_repo_preview
from .doctor import print_doctor
from .check_cli import run_check
from .help import print_help_topic, topic_names
from .wayland_portal import portal_environment, portal_screen_cast_available
from .portal_dbus import request_monitor_share, diagnose
from .screen_backend import detect_linux_screen_backend
from .screen_providers import discover_screen_providers, preferred_observe_provider
from .agent_session import AgentCapability, AgentSession
from .agent_executor import list_path, read_text, run_command
from .workspace import WorkspacePolicy
from .project_info import (
    PROJECT_URL,
    ISSUES_URL,
    CHANGELOG_URL,
    bundled_changelog,
)
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

    logs_parser = sub.add_parser(
        "logs",
        help="show Relmote's persistent per-user debug log",
    )
    logs_parser.add_argument(
        "--tail",
        type=int,
        default=100,
        help="number of recent log lines to show (default: 100)",
    )
    logs_parser.add_argument(
        "--path",
        action="store_true",
        help="print only the debug-log path",
    )
    def run_logs(args):
        path = log_path()
        if args.path:
            print(path)
            return 0
        print(f"Relmote debug log: {path}")
        print(
            "Privacy note: inspect before sharing; logs may contain "
            "hostnames, paths, network details, or error output."
        )
        content = tail_log(args.tail)
        if content:
            print()
            print(content, end="" if content.endswith("\n") else "\n")
        else:
            print("\nNo log entries yet.")
        return 0
    logs_parser.set_defaults(func=run_logs)

    about_parser = sub.add_parser(
        "about",
        help="show project links and build information",
    )
    def run_about(args):
        info = build_info()
        print(f'Relmote {info["display_version"]} (build {info["short_commit"]})')
        print(f'Source: {PROJECT_URL}')
        print(f'Issues: {ISSUES_URL}')
        print(f'Changelog: {CHANGELOG_URL}')
        return 0
    about_parser.set_defaults(func=run_about)

    changelog_parser = sub.add_parser(
        "changelog",
        help="show changes in the current development snapshot",
    )
    changelog_parser.set_defaults(
        func=lambda args: (print(bundled_changelog()) or 0)
    )

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
        print(f'Relmote {info["display_version"]} (build {build})')
        print(f'Channel: {info["channel"]}')
        print()
        print(f'Source:    {PROJECT_URL}')
        print(f'Issues:    {ISSUES_URL}')
        print(f'Changelog: {CHANGELOG_URL}')
        return 0
    version_parser.set_defaults(func=run_version)

    screen_parser = sub.add_parser(
        "screen",
        help="inspect or prepare screen-support capabilities",
    )
    screen_sub = screen_parser.add_subparsers(dest="screen_command", required=True)
    screen_probe = screen_sub.add_parser(
        "probe",
        help="check graphical session and ScreenCast portal readiness",
    )
    def run_screen_probe(args):
        screen = detect_linux_screen_backend()
        print("RELMOTE SCREEN PROBE\n")
        print(f"Session: {screen.session_type}")
        print(screen.note)
        if screen.session_type == "wayland":
            env = portal_environment()
            ok, message = portal_screen_cast_available()
            print(f"Runtime: {env.runtime_dir}")
            print(f"Session bus: {env.bus_address}")
            print(f"ScreenCast portal: {'ready' if ok else 'not ready'}")
            print(message)
            return 0 if ok else 1
        return 0 if screen.session_type == "x11" else 1
    screen_probe.set_defaults(func=run_screen_probe)

    screen_providers = screen_sub.add_parser(
        "providers",
        help="show available screen observation/control backends",
    )
    def run_screen_providers(args):
        print("RELMOTE SCREEN PROVIDERS\n")
        preferred = preferred_observe_provider()
        for item in discover_screen_providers():
            mark = "*" if preferred and item.provider_id == preferred.provider_id else " "
            state = "available" if item.available else "unavailable"
            abilities = []
            if item.observe:
                abilities.append("observe")
            if item.control:
                abilities.append("control")
            print(
                f"{mark} {item.provider_id:16} {state:11} "
                f"{'/'.join(abilities) or '-'}"
            )
            print(f"    {item.label} · consent: {item.consent}")
            print(f"    {item.note}")
        if preferred:
            print(f"\nPreferred observe provider: {preferred.provider_id}")
        else:
            print("\nNo screen-observe provider is currently available.")
        return 0
    screen_providers.set_defaults(func=run_screen_providers)


    screen_request = screen_sub.add_parser(
        "request",
        help="request a Wayland monitor share through the desktop portal",
    )
    def run_screen_request(args):
        print("Requesting screen share from the target desktop…")
        print("A GNOME screen-sharing chooser should appear on that computer.")
        response = request_monitor_share()
        print("Screen sharing approved.")
        print(response.results_text)
        print("PipeWire stream attachment is the next preview step.")
        return 0
    screen_request.set_defaults(func=run_screen_request)

    screen_debug = screen_sub.add_parser(
        "debug-portal",
        help="show which Wayland ScreenCast portal stage succeeds or fails",
    )
    def run_screen_debug(args):
        for line in diagnose():
            print(line, flush=True)
        return 0

    screen_debug.set_defaults(func=run_screen_debug)



    agent_parser = sub.add_parser(
        "agent",
        help="preview the scoped agent bridge",
    )
    agent_sub = agent_parser.add_subparsers(dest="agent_command", required=True)

    agent_list = agent_sub.add_parser("list", help="list an approved workspace path")
    agent_list.add_argument("root")
    agent_list.add_argument("path", nargs="?", default=".")
    def run_agent_list(args):
        policy = WorkspacePolicy.create(args.root)
        session = AgentSession(
            workspace=policy,
            controller="local-cli",
            capabilities=frozenset({AgentCapability.LIST}),
        )
        session.approve()
        for item in list_path(session, args.path):
            print(f"{item['type']:9} {item['name']}")
        return 0
    agent_list.set_defaults(func=run_agent_list)

    agent_read = agent_sub.add_parser("read", help="read a text file in an approved workspace")
    agent_read.add_argument("root")
    agent_read.add_argument("path")
    def run_agent_read(args):
        policy = WorkspacePolicy.create(args.root)
        session = AgentSession(
            workspace=policy,
            controller="local-cli",
            capabilities=frozenset({AgentCapability.READ}),
        )
        session.approve()
        print(read_text(session, args.path), end="")
        return 0
    agent_read.set_defaults(func=run_agent_read)

    agent_exec = agent_sub.add_parser("exec", help="run an allowlisted command in a workspace")
    agent_exec.add_argument("root")
    agent_exec.add_argument("tool", choices=("git", "pytest"))
    agent_exec.add_argument("tool_args", nargs="*")
    def run_agent_exec(args):
        policy = WorkspacePolicy.create(
            args.root,
            allowed_tools=frozenset({"git", "pytest"}),
        )
        session = AgentSession(
            workspace=policy,
            controller="local-cli",
            capabilities=frozenset({AgentCapability.EXEC}),
        )
        session.approve()
        result = run_command(session, [args.tool, *args.tool_args])
        if result["stdout"]:
            print(result["stdout"], end="")
        if result["stderr"]:
            print(result["stderr"], end="", file=sys.stderr)
        return result["returncode"]
    agent_exec.set_defaults(func=run_agent_exec)
    def _agent_remote_client(args):
        import os
        token = os.environ.get("RELMOTE_AGENT_TOKEN", "")
        if not token:
            raise RuntimeError(
                "Set RELMOTE_AGENT_TOKEN in the environment; "
                "do not pass the bearer token on the command line."
            )
        return RelmoteAgentClient(args.url, token)

    agent_host_cmd = agent_sub.add_parser(
        "host",
        help="show this machine's Agent Host identity and capabilities",
    )
    def run_agent_host(args):
        host = detect_agent_host()
        print("RELMOTE AGENT HOST")
        print(f"Name: {host.name}")
        print(f"Platform: {host.platform} / {host.architecture}")
        print("Capabilities:")
        for capability in host.capabilities:
            print(f"  - {capability}")
        print("Detected tools:")
        for tool in host.tools:
            print(f"  - {tool}")
        return 0
    agent_host_cmd.set_defaults(func=run_agent_host)

    agent_pair_cmd = agent_sub.add_parser(
        "pair",
        help="pair this controller/agent host with a Relmote target",
    )
    agent_pair_cmd.add_argument(
        "url",
        help="private Relmote Agent API URL, typically provided by the target",
    )
    agent_pair_cmd.add_argument(
        "--name",
        help="local name for this target profile",
    )
    def run_agent_pair(args):
        code = input("8-digit pairing code: ").strip()
        value = pair_agent(args.url, code)
        session = value["session"]
        target_name = args.name or session.get("controller") or session["session_id"][:8]
        path = save_profile(
            name=target_name,
            base_url=args.url,
            token=value["token"],
            session=session,
        )
        print(f"Paired with {target_name}.")
        print(f"Workspace: {session.get('workspace')}")
        print("Capabilities:")
        for capability in session.get("capabilities", []):
            print(f"  - {capability}")
        print(f"Connection profile: {path}")
        return 0
    agent_pair_cmd.set_defaults(func=run_agent_pair)

    paired_targets = PairedTargetService()

    agent_use = agent_sub.add_parser(
        "use",
        help="operate on a previously paired Relmote target",
    )
    agent_use.add_argument("target", help="paired target profile name")
    use_sub = agent_use.add_subparsers(dest="use_command", required=True)
    use_sub.add_parser("status")
    use_list = use_sub.add_parser("list")
    use_list.add_argument("path", nargs="?", default=".")
    use_read = use_sub.add_parser("read")
    use_read.add_argument("path")
    use_exec = use_sub.add_parser("exec")
    use_exec.add_argument("tool", choices=("git", "pytest"))
    use_exec.add_argument("tool_args", nargs="*")

    def run_agent_use(args):
        if args.use_command == "status":
            print(__import__("json").dumps(paired_targets.status(args.target), indent=2))
            return 0
        if args.use_command == "list":
            print(
                __import__("json").dumps(
                    paired_targets.list(args.target, args.path),
                    indent=2,
                )
            )
            return 0
        if args.use_command == "read":
            print(paired_targets.read(args.target, args.path), end="")
            return 0
        if args.use_command == "exec":
            result = paired_targets.exec(
                args.target,
                [args.tool, *args.tool_args],
            )
            if result.get("stdout"):
                print(result["stdout"], end="")
            if result.get("stderr"):
                print(result["stderr"], end="", file=__import__("sys").stderr)
            return int(result.get("returncode", 1))
        raise ValueError("unknown paired-target command")

    for use_parser in use_sub.choices.values():
        use_parser.set_defaults(func=run_agent_use)

    agent_targets = agent_sub.add_parser(
        "targets",
        help="list locally paired Relmote targets",
    )
    def run_agent_targets(args):
        targets = paired_targets.targets()
        if not targets:
            print("No paired Relmote targets.")
            return 0
        for target in targets:
            print(
                f"{target['name']}  "
                f"{target.get('workspace') or '?'}  "
                f"{target.get('state') or '?'}"
            )
        return 0
    agent_targets.set_defaults(func=run_agent_targets)

    agent_remote = agent_sub.add_parser(
        "remote",
        help="test an approved Agent API from another machine",
    )
    agent_remote.add_argument("--url", required=True)
    remote_sub = agent_remote.add_subparsers(dest="remote_command", required=True)

    remote_session = remote_sub.add_parser("session")
    remote_list = remote_sub.add_parser("list")
    remote_list.add_argument("path", nargs="?", default=".")
    remote_read = remote_sub.add_parser("read")
    remote_read.add_argument("path")
    remote_exec = remote_sub.add_parser("exec")
    remote_exec.add_argument("tool", choices=("git", "pytest"))
    remote_exec.add_argument("tool_args", nargs="*")

    def run_agent_remote(args):
        client = _agent_remote_client(args)
        if args.remote_command == "session":
            print(__import__("json").dumps(client.session(), indent=2))
            return 0
        if args.remote_command == "list":
            print(__import__("json").dumps(client.list(args.path), indent=2))
            return 0
        if args.remote_command == "read":
            print(client.read(args.path), end="")
            return 0
        if args.remote_command == "exec":
            result = client.exec([args.tool, *args.tool_args])
            if result.get("stdout"):
                print(result["stdout"], end="")
            if result.get("stderr"):
                print(result["stderr"], end="", file=__import__("sys").stderr)
            return int(result.get("returncode", 1))
        raise ValueError("unknown remote agent command")

    for remote_parser in (remote_session, remote_list, remote_read, remote_exec):
        remote_parser.set_defaults(func=run_agent_remote)

    agent_enable = agent_sub.add_parser(
        "enable",
        help="enable private Agent API access through the detected transport",
    )
    def run_agent_enable(args):
        print("Enabling private Relmote Agent access...")
        result = enable_private_transport()
        print(result.get("detail") or "Agent access enabled.")
        return 0
    agent_enable.set_defaults(func=run_agent_enable)

    agent_status_cmd = agent_sub.add_parser(
        "status",
        help="show Agent API private transport status",
    )
    def run_agent_status(args):
        info = serve_status()
        print("RELMOTE AGENT ACCESS")
        print(f"Tailscale: {'available' if info.get('available') else 'unavailable'}")
        print(f"Private transport: {'ON' if info.get('enabled') else 'OFF'}")
        return 0
    agent_status_cmd.set_defaults(func=run_agent_status)

    agent_disable = agent_sub.add_parser(
        "disable",
        help="disable Relmote's private Agent API transport",
    )
    def run_agent_disable(args):
        disable_private_transport()
        print("Relmote Agent private transport disabled.")
        return 0
    agent_disable.set_defaults(func=run_agent_disable)

    agent_transport_cmd = agent_sub.add_parser(
        "transport",
        help="show an explicit private transport for the Agent API",
    )
    def run_agent_transport(args):
        info = tailscale_transport()
        print("RELMOTE AGENT TRANSPORT\n")
        print(info["message"])
        if not info["available"]:
            return 1
        print(f"\nEnable:  {info['command']}")
        print(f"Status:  {info['status_command']}")
        print(f"Disable: {info['disable_command']}")
        return 0
    agent_transport_cmd.set_defaults(func=run_agent_transport)

    agent_scope_cmd = agent_sub.add_parser(
        "scope",
        help="classify how broad a proposed Agent workspace is",
    )
    agent_scope_cmd.add_argument("root")
    def run_agent_scope(args):
        info = classify_scope(args.root)
        print(f"{info['level'].upper()}: {info['label']}")
        print(info["message"])
        return 0
    agent_scope_cmd.set_defaults(func=run_agent_scope)


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
    configure_logging()
    args = build_parser().parse_args()
    if args.command is None:
        return run_app()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
