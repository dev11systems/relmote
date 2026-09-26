from __future__ import annotations

from .runtime import RelmoteRuntime
from .help import render_help


def render_home(
    runtime: RelmoteRuntime,
    *,
    web_url: str = "http://127.0.0.1:8787",
    web_ready: bool = False,
    web_exposure: str = "This computer only",
) -> str:
    value = runtime.snapshot()
    session = value.get("session")
    checks = (
        "ON"
        if session and not session.get("revoked")
        else "OFF"
    )
    remote = value.get("support", {})
    support = "ON" if remote.get("available") else "OFF"
    return "\n".join(
        [
            "RELMOTE",
            "",
            value["target"]["name"],
            f"Local checks:   {checks}",
            f"Remote support: {support}",
            "",
            "1  Check this computer",
            "2  Network diagnosis",
            "3  Storage overview",
            f"Web interface: {'Ready' if web_ready else 'Unavailable'}",
            f"  {web_url}" if web_ready else "",
            f"  {web_exposure}" if web_ready else "",
            "",
            "4  Web interface",
            "5  Remote support settings",
            "h  Help",
            "q  Quit",
        ]
    )


def run_simple_tui(
    runtime: RelmoteRuntime,
    *,
    web_url: str = "http://127.0.0.1:8787",
    web_ready: bool = False,
    web_exposure: str = "This computer only",
) -> int:
    """Dependency-free preview TUI.

    This intentionally starts as a simple terminal menu. A richer TUI framework
    can replace the renderer without changing runtime semantics.
    """
    while True:
        print("\033[2J\033[H", end="")
        print(render_home(
            runtime,
            web_url=web_url,
            web_ready=web_ready,
            web_exposure=web_exposure,
        ))
        choice = input("\n> ").strip().lower()

        if choice == "q":
            return 0
        if choice == "4":
            if web_ready:
                print("\nWEB INTERFACE\n")
                print(web_url)
                print(f"\nConnection: {web_exposure}")
                print("\nOpen this address in a browser on an authorized device.")
                print("Relmote must keep running while you use the web interface.")
            else:
                print("\nWeb interface is unavailable.")
                print("Try: relmote doctor")
            input("\nPress Enter to return to Relmote.")
            continue
        if choice == "h":
            input("\n" + render_help() + "\nPress Enter to continue.")
            continue
        if choice == "5":
            current = runtime.snapshot()["support"]
            print("\nREMOTE SUPPORT\n")
            print("This controls whether remote support is permitted.")
            print("It does not configure Tailscale/SSH/network exposure by itself.\n")
            print(f"Current: {'ON' if current['available'] else 'OFF'} ({current['mode']})")
            print("\n1  Enable until I turn it off")
            print("2  Enable for 1 hour")
            print("3  Disable support")
            print("b  Back")
            support_choice = input("\n> ").strip().lower()
            if support_choice == "1":
                runtime.enable_support_until_disabled()
            elif support_choice == "2":
                runtime.enable_support_for(3600)
            elif support_choice == "3":
                runtime.disable_support()
            continue

        snapshot = runtime.snapshot()
        session = snapshot.get("session")
        if not session or session.get("revoked"):
            runtime.start_checks()

        task = {
            "1": "full-check",
            "2": "diagnose-network",
            "3": "storage-overview",
        }.get(choice)
        if task:
            runtime.run_task(task)
            latest = runtime.snapshot()["tasks"][-1]
            print("\nRESULT\n")
            for finding in latest.get("findings", []):
                print(f"[{finding['status']}] {finding['statement']}")
                if finding.get("uncertainty"):
                    print(f"  {finding['uncertainty']}")
            input("\nPress Enter to continue.")
