from __future__ import annotations

from dataclasses import dataclass

from .agent import AgentObservation, LocalAgent


@dataclass(frozen=True)
class DiagnosticFinding:
    status: str
    statement: str
    evidence: tuple[str, ...]
    uncertainty: str | None = None


@dataclass(frozen=True)
class DiagnosticReport:
    name: str
    findings: tuple[DiagnosticFinding, ...]
    observations: tuple[AgentObservation, ...]


def diagnose_network(agent: LocalAgent) -> DiagnosticReport:
    network = agent.observe("network.inspect")
    dns = agent.observe("network.dns")

    findings: list[DiagnosticFinding] = []
    addresses = network.data.get("addresses", [])
    configured = [x for x in addresses if x.get("kind") == "configured"]
    link_local = [x for x in addresses if x.get("kind") == "link-local"]

    if configured:
        findings.append(
            DiagnosticFinding(
                "observed",
                f"{len(configured)} non-loopback configured address(es) were observed.",
                ("network.inspect",),
                "S2 does not yet enumerate every interface or route portably.",
            )
        )
    elif link_local:
        findings.append(
            DiagnosticFinding(
                "attention",
                "Only link-local addressing was observed.",
                ("network.inspect",),
                "This can be consistent with missing normal address configuration, but S2 has not tested DHCP or routing.",
            )
        )
    else:
        findings.append(
            DiagnosticFinding(
                "unknown",
                "No non-loopback address was observed through the current portable adapter.",
                ("network.inspect",),
                "This is not proof that the machine has no usable network interface.",
            )
        )

    servers = dns.data.get("servers", [])
    if servers:
        findings.append(
            DiagnosticFinding(
                "observed",
                f"Resolver configuration lists {len(servers)} DNS server(s).",
                ("network.dns",),
                "Configured DNS servers have not been actively tested.",
            )
        )
    else:
        findings.append(
            DiagnosticFinding(
                "attention",
                "No DNS server was found in the currently supported resolver configuration source.",
                ("network.dns",),
                "Some operating systems or resolver stacks store this information elsewhere.",
            )
        )

    findings.append(
        DiagnosticFinding(
            "not-tested",
            "Internet reachability was not tested.",
            (),
            "Observe mode performs no external network probe by default.",
        )
    )

    return DiagnosticReport(
        name="diagnose-network",
        findings=tuple(findings),
        observations=(network, dns),
    )
