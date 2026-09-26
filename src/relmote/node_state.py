from __future__ import annotations

from dataclasses import dataclass, field

from .modules import ModuleDescriptor
from .topology import Node, Target, reachability


@dataclass
class NodeState:
    node: Node
    targets: dict[str, Target] = field(default_factory=dict)
    modules: dict[str, ModuleDescriptor] = field(default_factory=dict)

    def snapshot(self) -> dict:
        return {
            "node": {
                "node_id": self.node.node_id,
                "name": self.node.name,
                "reachability": reachability(self.node.controller_paths).value,
                "controller_paths": [
                    {
                        "path_id": path.path_id,
                        "transport": path.transport,
                        "interactive": path.interactive,
                        "constrained": path.constrained,
                        "encrypted": path.encrypted,
                        "authenticated": path.authenticated,
                        "bandwidth_bps": path.bandwidth_bps,
                        "latency_ms": path.latency_ms,
                    }
                    for path in self.node.controller_paths
                ],
            },
            "targets": [
                {
                    "target_id": target.target_id,
                    "name": target.name,
                    "system_paths": [
                        {
                            "path_id": path.path_id,
                            "transport": path.transport,
                            "feedback": path.feedback.value,
                            "works_before_os": path.works_before_os,
                            "native": path.native,
                            "bidirectional": path.bidirectional,
                        }
                        for path in target.system_paths
                    ],
                }
                for target in self.targets.values()
            ],
            "modules": [
                {
                    "module_id": module.module_id,
                    "vendor": module.vendor,
                    "product": module.product,
                    "capabilities": list(module.capabilities),
                }
                for module in self.modules.values()
            ],
        }
