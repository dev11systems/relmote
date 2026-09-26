from __future__ import annotations

from .runtime import RelmoteRuntime
from .help import render_help


def render_home(
    runtime: RelmoteRuntime,
    *,
    web_url: str = "http://127.0.0.1:8787",
    web_ready: bool = False,
) -> str:
    value = runtime.snapshot()
    session = value.get("session")
    support = (
        "Checks enabled"
        if session and not session.get("revoked")
        else "Checks off"
    )
    return "\n".join(
        [
            "RELMOTE",
            "",
            value["target"]["name"],
            f"Support checks: {support}",
            "",
            "1  Check this computer",
            "2  Network diagnosis",
            "3  Storage overview",
            f"Web interface: {'Ready' if web_ready else 'Unavailable'}",
            f"  {web_url}" if web_ready else "",
            "",
            "4  Open web interface",
            "h  Help",
            "q  Quit",
        ]
    )


def run_simple_tui(
    runtime: RelmoteRuntime,
    *,
    web_url: str = "http://127.0.0.1:8787",
    web_ready: bool = False,
) -> int:
    """Dependency-free preview TUI.

    This intentionally starts as a simple terminal menu. A richer TUI framework
    can replace the renderer without changing runtime semantics.
    """
    while True:
        print("\033[2J\033[H", end="")
        print(render_home(runtime, web_url=web_url, web_ready=web_ready))
        choice = input("\n> ").strip().lower()

        if choice == "q":
            return 0
        if choice == "4":
            message = (
                f"Web interface: {web_url}"
                if web_ready
                else "Web interface is unavailable. Try relmote doctor."
            )
            input(f"\n{message}\nPress Enter to continue.")
            continue
        if choice == "h":
            input("\n" + render_help() + "\nPress Enter to continue.")
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
