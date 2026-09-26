from __future__ import annotations

from dataclasses import dataclass

from .agent import AgentObservation, LocalAgent
from .diagnostics import DiagnosticFinding, DiagnosticReport, diagnose_network


@dataclass(frozen=True)
class FullCheckSection:
    name: str
    findings: tuple[DiagnosticFinding, ...]


def linux_full_check(agent: LocalAgent) -> DiagnosticReport:
    observations: list[AgentObservation] = []

    for capability in (
        "system.identify",
        "system.platform",
        "system.memory",
        "system.uptime",
        "hardware.cpu",
        "storage.inspect",
        "network.inspect",
        "network.dns",
        "platform.native",
    ):
        observations.append(agent.observe(capability))

    findings: list[DiagnosticFinding] = []

    platform_obs = next(x for x in observations if x.capability == "platform.native")
    native = platform_obs.data.get("observations", {})
    linux_os = native.get("linux.os", {})
    pretty = linux_os.get("pretty_name")
    if pretty:
        findings.append(
            DiagnosticFinding(
                "observed",
                f"Operating system: {pretty}.",
                ("platform.native",),
            )
        )

    memory = next(x for x in observations if x.capability == "system.memory")
    physical = memory.data.get("physical_bytes")
    if physical:
        findings.append(
            DiagnosticFinding(
                "observed",
                f"Physical memory: {physical / (1024 ** 3):.1f} GiB.",
                ("system.memory",),
            )
        )


    cpu = next(x for x in observations if x.capability == "hardware.cpu")
    cpu_name = cpu.data.get("model") or cpu.data.get("processor")
    cpu_count = cpu.data.get("logical_cpu_count") or cpu.data.get("count")
    if cpu_name or cpu_count:
        detail = cpu_name or "Processor"
        if cpu_count:
            detail += f" · {cpu_count} logical CPU(s)"
        findings.append(
            DiagnosticFinding(
                "observed",
                detail + ".",
                ("hardware.cpu",),
            )
        )

    uptime = next(x for x in observations if x.capability == "system.uptime")
    seconds = uptime.data.get("uptime_seconds")
    if seconds is not None:
        days = seconds / 86400
        findings.append(
            DiagnosticFinding(
                "observed",
                f"System uptime: {days:.1f} day(s).",
                ("system.uptime",),
            )
        )

    storage = next(x for x in observations if x.capability == "storage.inspect")
    percent = storage.data.get("percent_used")
    if percent is not None:
        status = "attention" if percent >= 90 else "observed"
        total = storage.data.get("total_bytes")
        free = storage.data.get("free_bytes")
        capacity_note = ""
        if total is not None and free is not None:
            capacity_note = (
                f" Total {total / (1024 ** 3):.1f} GiB; "
                f"{free / (1024 ** 3):.1f} GiB free."
            )
        findings.append(
            DiagnosticFinding(
                status,
                f"Primary filesystem is {percent:.1f}% used." + capacity_note,
                ("storage.inspect",),
                "High utilization can cause application/system problems."
                if status == "attention" else None,
            )
        )

    services = native.get("linux.services", {})
    failed_count = services.get("failed_service_count")
    if failed_count is not None:
        findings.append(
            DiagnosticFinding(
                "attention" if failed_count else "observed",
                (
                    f"{failed_count} failed system service(s) were observed."
                    if failed_count
                    else "No failed system services were reported by systemd."
                ),
                ("platform.native",),
                None if services.get("available") else "systemd status unavailable",
            )
        )

    network_report = diagnose_network(agent)
    findings.extend(network_report.findings)

    return DiagnosticReport(
        name="full-check",
        findings=tuple(findings),
        observations=tuple(observations),
    )
