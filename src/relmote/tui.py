from __future__ import annotations

from .runtime import RelmoteRuntime


def render_home(runtime: RelmoteRuntime) -> str:
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
            "4  Open web interface",
            "q  Quit",
        ]
    )


def run_simple_tui(
    runtime: RelmoteRuntime,
    *,
    web_url: str = "http://127.0.0.1:8787",
) -> int:
    """Dependency-free preview TUI.

    This intentionally starts as a simple terminal menu. A richer TUI framework
    can replace the renderer without changing runtime semantics.
    """
    while True:
        print("\033[2J\033[H", end="")
        print(render_home(runtime))
        choice = input("\n> ").strip().lower()

        if choice == "q":
            return 0
        if choice == "4":
            input(f"\nWeb interface: {web_url}\nPress Enter to continue.")
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
