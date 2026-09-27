# Architecture decisions

Compact record of durable decisions.

- **D001 — Relmote is a platform.** Nodes may be hardware, software, virtual, embedded, recovery, or hybrid.
- **D002 — AI is optional.** AI is a planner, never the fundamental authority layer.
- **D003 — Tasks live above transports.** A task may survive controller/system path changes.
- **D004 — Observation differs from interpretation.** Actions are not evidence; blind HID creates no observation.
- **D005 — Connectivity is not authorization.** Reachability, identity, authentication, authorization, capability, and evidence remain separate.
- **D006 — Hardware when useful, software when sufficient.** Do not require Pocket if Agent solves the problem; do not require Agent if physical interfaces solve it.
- **D007 — Physical target output has an independent safety plane.**
- **D008 — Modules advertise capability, not authority.** Third-party modules are untrusted peripherals.
- **D009 — Open compatibility.** No Dev11 permission, cloud activation, or proprietary certification token is required for compatible implementations.
- **D010 — Base Pocket stays small.** Niche/bulky/high-power interfaces belong in modules/plugins where practical.
- **D011 — Owner-controlled identity.** A Dev11 account is optional convenience, not the root of ownership.
- **D012 — Recovery must not be a vendor backdoor.**
- **D013 — Do not freeze hardware connectors prematurely.** Stabilize logical interfaces first.
- **D014 — Build before polishing everything.** Immediate milestone is real HID + physical authorization/STOP.
- **D015 — No silent external metadata side effects.** Transport activation must not publish durable identifiers, request publicly logged certificates, create public ingress, or register with third-party control infrastructure without explicit informed consent. Prefer an equally useful lower-disclosure path when available.
- **D016 — Roles may co-locate without collapsing authority.** Controller, Agent Host, Hub, and Target are logical roles rather than mandatory physical machines. A Hub and Agent Host may share one host for operational convenience, but co-location must not imply credential or authority inheritance.
