# Coherent Relmote vNext — modular, adaptive, resilient access

> **Research proposal · 2026-10-29 · Author review pending**
>
> This is **not** an adopted hardware specification, a release plan, a security certification, or evidence of tested recovery/satellite hardware. It proposes extensions to the existing Relmote platform while preserving documented current implementation status and hardware validation gates.

## Executive thesis

Relmote already describes a user-controlled, capability-aware interface platform implemented as software, physical hardware, or both. This proposal treats recovery, low-tech access, alternative power, satellite messaging, and optional intelligence as **profiles of that same platform**, not separate mandatory products or competing repositories.

**Design test:** As power, bandwidth, devices, human support, and connectivity change, does the system preserve the *smallest safe useful capability* while making the actual constraints, permissions, and fallbacks understandable?

A device should become more capable when circumstances permit without becoming useless when circumstances deteriorate. This must not mean that degraded conditions justify weaker permissions, covert control, or access to secrets.

## Source-of-truth and status

Reviewed against the repository default branch at commit [5e7123b](https://github.com/dev11systems/relmote/commit/5e7123beaa82eb6fe62477f21c888f59355d66d6).

- [Current status](../STATUS.md) is authoritative for implementation claims; it records an exercised Linux software preview and experimental Hub/portal work, while hardware validation remains planned.
- [Roadmap](../ROADMAP.md) retains physical AUTHORIZE/STOP validation, sacrificial HID testing, and measured stop latency as outstanding hardware gates.
- [Decisions](../DECISIONS.md) D001–D016 remain the established architecture (including optional AI, independent safety, open compatibility, owner-controlled identity, and no silent metadata side effects).
- [Platform model](../PLATFORM-MODEL.md), [architecture](../ARCHITECTURE.md), [transports](../TRANSPORTS.md), [power](../POWER.md), [modularity](../MODULARITY.md), [recovery](../RECOVERY.md), and [UX principles](../UX-PRINCIPLES.md) already cover many ideas explored here.
- The [module interface v0.1](../../spec/relmote-module-v0.1.md) is a draft. Pins, physical contacts, power limits, high-speed interfaces, stacking, and certification are not frozen.
- The [Pocket mechanical study](../../hardware/industrial-design/pocket-envelope-v0.1.md) proposes **150 × 72 × 18 mm** with two 68 × 68 mm rear S-zones (or one 68 × 140 mm L-module), **not** a validated enclosure. A separately explored roughly 125 × 90 mm recovery-node concept is **not** automatically substituted for that envelope.
- The [compute study](../../hardware/component-studies/application-compute-v0.1.md) favors efficient embedded Linux for Pocket and regards CM5/RK3588-class compute as candidates more naturally suited to All-in-One/accelerator use; no production SOM is selected.
- [Internal safety protocol](../../spec/internal-safety-protocol-v0.1.md) and [safety MCU study](../../hardware/component-studies/safety-mcu-v0.1.md) emphasize bounded actions, physical STOP, explicit leases, replay resistance, and a narrow hardware-facing trust boundary. Exact cryptographic protocol remains open.

Nothing in this proposal supersedes those documents. It should be reviewed before translating any item into a normative requirement.

## What is retained vs. extended

| Existing Relmote foundation | Retain | Candidate vNext research |
| --- | --- | --- |
| Hardware, software, hybrid node roles | Roles not bound to specific enclosures | Portable *recovery profile* of the same node model |
| Separate controller and target transports | Reachability never grants authority | Telephone/DTMF/SMS and satellite/mesh entry adapters |
| Distinct Agent Host, Controller, Node/Target, optional Hub | No co-location-based permission inheritance | Off-site recovery broker remains a separate, non-authoritative service |
| Observe / Teach / Assist / Operate | Clear, revocable scoped grants | Accessible modality changes and low-tech read-only fallback |
| MCU target-output safety plane | Physical STOP, leases, fail closed | Independent credential-security boundary **in addition to** target safety |
| Optional replaceable power, sleep states | Batteryless USB-C use remains supported | Passive reader-powered, harvested-burst, and full-Linux energy tiers |
| Snap modules + ordinary external USB-C | Open module compatibility; no proprietary blessing | Field satellite accessory, external power/harvester and protected storage |
| Owner recovery key, other controllers, future recovery quorum | No vendor recovery backdoor | Device-loss and zero-possession recovery scenarios, separate from other providers' accounts |
| Progressive, plain-language UX | Complexity by choice | Capability presentation based on context without opaque automatic escalation |

## Proposed system boundaries

The following are *logical functions*, not a demand for a separate PCB for each:

1. **Human access / controller:** local tactile buttons and status display, USB, web/CLI, optional phone voice/keypad, or a companion device. Each channel declares input limits and trust provenance. AI voice, if offered, is optional.
2. **Node identity, sessions and authorization:** an independently enforced policy for principals, target identity, task scope, expiry, revocation and evidence. No channel or model may manufacture owner authority.
3. **Replaceable compute plane:** Linux application, optional local/remote AI planner, routing, richer diagnostics and UI. Power-gated or unavailable in low-energy mode.
4. **Physical safety plane:** minimal safety MCU controls target-facing output (HID and later others), AUTHORIZE, STOP, watchdog and electrical safety. Commands are structured and bounded, not natural-language instructions.
5. **Credential/recovery security boundary:** separately reviewed storage/key handling, local confirmation, and owner-approved recovery operations. It is **not assumed** that the HID safety MCU also protects general vault secrets. A secure element or other trustworthy authenticator is a candidate, not a frozen selection.
6. **Connectivity/power modules:** interchangeable and discoverable transport or supply capabilities, each with admission, safety, disclosure and power constraints.
7. **Optional off-site services:** relay/rendezvous, satellite backend, guardian approvals or recovery coordinator. These facilitate *communication*, not automatic identity proof or privilege.

The existing software Node/Agent Host/Hub topology remains valid and useful with **no physical Relmote**.

## Coherent Design requirements for evaluation

- **Unburdensome default:** a functional core without requiring an AI provider, cloud subscription, public account, specialist module, or always-on Linux.
- **Depth on demand:** Reveal extra capabilities without forcing configuration or advanced vocabulary on the ordinary user.
- **Legible adaptation:** Surface why an operation is unavailable (no power, no credential, radio restricted, insufficient bandwidth, lack of authority) and the alternatives that actually exist.
- **Optional physical complexity:** Standard USB-C modules remain valid even when proprietary-style snap geometry would be aesthetically cleaner.
- **Meaningful consent and stop:** No automatic privilege gain when switching from local USB to LTE, LoRa, satellite, remote browser or AI.
- **Continuity without false equivalence:** Preserve task identifiers and intent across transport changes, but explicitly mark loss of confidentiality, feedback, authentication or reliability.
- **Respect for human difference:** Keypad, speech, tactile controls, screen reader, text, physical assistance and non-AI modes are potential alternatives—not universally equivalent pathways.
- **Owner agency, repairability and portability:** No vendor-controlled boot or mandatory cloud dependency; physical and software failures must have documented exit/recovery paths.
- **No stealth controls:** A public recovery-information site is not permission to disguise computer-control behavior or hide active Relmote sessions.

## Hardware family: proposed roles rather than compulsory SKUs

| Form | Preferred role | What remains optional |
| --- | --- | --- |
| **Mini** | Low-power protocol/safety or passive authenticator variant | Linux, always-on connectivity, display size |
| **Pocket** | Everyday portable node for USB/Wi-Fi/BLE, observable safe controls | Cellular, GNSS, expanded storage, extra battery |
| **All-in-One** | More room for compute, KVM/serial, power and operator feedback | Heavy local AI, integrated radios |
| **Field** | Adverse environments; external antennas, satellite/mesh, energy harvesting, ruggedization | Broadband terminal, larger battery, auxiliary displays |
| **Dock** | Stationary power, Ethernet/PoE, keyboard/video, bench/debug and adapters | Continuous operation, high-power modules |

**Recovery** is a *profile* usable on compatible hardware, not necessarily a sixth device. An external off-site recovery service can provide parts of the same workflow even if every Relmote device is lost.

### Physical and RF constraints

Pocket's reference S-module geometry (68 × 68 mm) is **not guaranteed to fit** a chosen satellite radio/antenna. Antenna keep-outs, open-sky orientation, RF coexistence, insertion losses, battery placement, stacking height, temperature, regional certification and operator support must be measured. If an integrated satellite assembly invalidates an existing radio certification or the Pocket envelope, prefer a **Field module, externally cabled antenna, or standalone gateway** rather than silently rewriting the Pocket mechanical standard.

No universal “satellite internet” claim: satellite-IoT short messages, direct-to-cell services and broadband satellite terminals are very different products. Coverage, clear-sky conditions, jurisdiction and subscription can all block delivery.

## Energy-adaptive operating tiers

The [existing power study](../../hardware/industrial-design/pocket-power-budget-v0.1.md) gives indicative rather than measured ranges. vNext should evaluate *joules per completed useful operation* and wake/recovery latency in addition to runtime.

| Tier | Energy source | What is realistically useful | Hard limit |
| --- | --- | --- | --- |
| **Passive** | Reader-supplied USB/NFC energy | Enrolled cryptographic authentication or static printed/e-paper public recovery instructions | No powered Linux or satellite transmission without an additional supply |
| **Intermittent / MCU** | Small cell, harvested energy buffered in capacitor/cell, or external input | Simple status, signed short request, store/forward or wake control | Requires sufficient energy for modem peaks and a reachable service |
| **Linux active** | Sustained USB-C, replaceable battery, dock, adequate field supply | UI, encrypted workspace, USB networking, richer diagnostics and optional models | Thermal and energy budgets constrain operation |
| **Expanded / dock** | Larger power pack, PoE/dock, regulated vehicle/solar supply | KVM/high-bandwidth or heavy compute where authorized | Connector, antenna, heat and supply budgets remain explicit |

Potential inputs to research: USB-C, removable cell, solar + charge regulator, supercapacitors, human-powered generator, dock/vehicle power. **A battery-optional platform is not a promise of batteryless operation in every environment.** Movement/body-heat/RF harvesting should not be represented as a realistic primary supply for Linux or satellite TX without empirical evidence.

Power-source attachment must never imply target authorization; avoid unintended USB backfeeding. STOP and safe disarm must be tested through brownouts and controller loss.

## Communications and identity: what goes where

### Transport adapters

- **Local**: USB gadget/network, Wi-Fi AP, BLE, serial and ordinary local UI.
- **Infrastructure-dependent**: cellular data/SMS, SIP/voice gateway, private networks, remote browsers.
- **Constrained/off-grid**: LoRa/Meshtastic/MeshCore or satellite-IoT via separately supported modules/backends.

Transport descriptors should eventually make **direction, payload limits, reliability, interactivity, link cost, power cost, regulatory restrictions, metadata disclosure, authentication/encryption, and actual evidence** visible. The exact schema is for later review; do **not** freeze new descriptor fields in this PR.

A request over satellite or SMS is a message, **not an authorization**. Use explicit message IDs, expiry, replay resistance, authenticated acknowledgements and bounded action types. Incoming voice, keypad and natural-language commands can start a recovery case without being proof of owner identity.

### Separate the recovery problems

1. **Relmote node ownership recovery** — already addressed conceptually in [identity recovery](../RECOVERY.md): replacement controller, recovery material, local node reset, future quorum. A node reset can erase identity and should visibly break old trust.
2. **Other accounts and finances** — 1Password, email, banking and similar external systems each have their own authenticators and institution-controlled recovery rules. A new phone, a Relmote node, or authenticated access to Relmote does **not** automatically restore these accounts.
3. **Physical zero-possession recovery** — if someone has no devices, identifiers or credentials, they might still initiate a *restricted* help case through a borrowed phone, an internet endpoint or a recognized human. Guardians can offer independently authenticated, purpose-bound attestations or assistance, but cannot manufacture bank access or impersonate the account owner.
4. **Emergency purchasing power** — assistance may take the form of a guardian voluntarily paying a verified local merchant for an essential item. This is **not** the same as restoring access to the claimant's own financial account, nor is it permission for AI to move money.

The physical recovery device may hold an **encrypted, selectively scoped recovery capsule**, but must not become a single unprotected collection of master passwords. Keep a genuinely independent off-site/exportable recovery route. No actual secrets, addresses, contacts, private machine identifiers or personal circumstances belong in public repository examples.

### Two important threat models

- **Untrusted borrowed endpoint:** A remote VM can protect its own storage, not the borrowed host's keyboard, screen or browser. Prefer sensitive approvals on the device's own protected interface; do not present a compromised terminal as “secure” merely because a session is ephemeral.
- **Physical coercion / social recovery:** Recognizing the correct person does not prove their request is freely chosen. Delay and constrain high-risk changes, use independent review where appropriate, and offer humane non-guardian alternatives without making any one person a gatekeeper.

## Candidate capability-to-module map

| Feature | Baseline location | Optional implementation | Boundaries |
| --- | --- | --- | --- |
| Target HID + STOP | Safety MCU / target adapter | Mini/Pocket | Must meet existing bench stop/replay tests |
| Scoped owner approval | Existing Node policy | Local input, Controller UI | Not delegated to planner or third-party module |
| Passive authentication | Separate approved authenticator | NFC/USB accessory | Reader-power required; service must enroll key |
| Recovery capsule | Encrypted storage and independent off-site backup | Recovery/storage module | No plaintext on untrusted screen |
| USB local management | Linux/software Node | USB gadget, external adapter | Port role, power and grants distinct |
| LoRa/mesh | Existing constrained transport abstraction | S module or external | Regional RF rules; limited payload |
| Satellite-IoT messages | Future constrained transport adapter | Field/external module | Sky, service, antenna, cert and energy constraints |
| Voice / DTMF / SMS | Optional controller gateway | ToneLine-like external service | Transcript is not credential proof |
| Continuity across channels | Session/task layer | Uniline-like adapter | Session re-auth on trust changes |
| Solar / generator / battery | Power board or external source | Field/power module | Measured cold-start, safe stop |
| AI reasoning | Optional planner/Agent Host | Local, home, cloud | Explicit routing and disclosure; no privileged authority |
| Terminal/screen/KVM | Existing separate capabilities | Target software / KVM module | Observe never implies control |

This table maps **where features may belong**, not the existence or readiness of any particular module.

## Decision ledger for author review

| ID | Status | Design position | Evidence / question |
| --- | --- | --- | --- |
| C01 | **Retain existing** | Platform remains software/hardware/hybrid | D001, D006; no hardware dependency |
| C02 | **Retain existing** | Separate target safety/STOP from Linux and planners | D002, D007; bench tests remain incomplete |
| C03 | **Proposed** | Recovery is a profile, not a separate mandatory hardware product | Compare actual module/role contracts |
| C04 | **Proposed** | Distinct security boundary for recovery credentials | Audit hardware/cryptography; avoid custom crypto |
| C05 | **Proposed** | Explicit passive, intermittent and Linux energy tiers | Cold-start, brownout and TX measurements |
| C06 | **Proposed** | Satellite-IoT belongs to Field/external expansion first | RF/antenna/certification/operator validation |
| C07 | **Proposed** | Phone and alternate input gateways are controller adapters | Separate caller/session identity from channel |
| C08 | **Retain existing** | Recovery must not introduce a Dev11/vendor backdoor | D011–D012; preserve exported independent backups |
| C09 | **Open** | Whether Pocket needs an integrated cryptographic authenticator | Physical-space, secure-element and lifecycle study |
| C10 | **Open** | Which context/capability selection rules require explicit consent | Accessibility and disclosure testing |
| C11 | **Open** | Owner-controlled secure boot/key recovery without DIY lockout | Security/repairability trade-off |
| C12 | **Retain existing** | No custom PCB before validated transport/safety/companion model | D014 and hardware strategy |
| C13 | **Open** | Interface geometry for satellite/power module | Existing S/L envelopes and RF/thermal constraints |
| C14 | **Open** | What recovery can accomplish with no possessions and no witnesses | Do not assert impossible assurance or universal service |

“Proposed” is intentionally **not** “accepted”. This document does not add new entries to the authoritative [decisions ledger](../DECISIONS.md) until reviewed.

## Validation and prototype sequence

1. **Gate A — Source reconciliation.** Review this proposal against canonical docs, mark redundancies and distinguish new requirements from prior commitments; preserve public/general examples.
2. **Gate B — Existing hardware MVP-1.** Complete [Pi Zero HID bench validation](../../hardware/v0.1-pi-zero/BRINGUP.md), including real physical STOP, replay, expiry, failure and measurable stop latency on a sacrificial target. No recovery secret or public radio needed.
3. **Gate C — Separation of trust boundaries.** With mocked data, test protected local confirmation, Linux crash/reboot, unauthorized module commands, and lost-controller behavior. Show target safety remains independent of credential handling.
4. **Gate D — Recovery interface simulation.** Mock an untrusted borrowed terminal, an ordinary telephone/keypad, a guardian case, and a new device with zero saved account credentials. Test that an unverified session never yields secrets or broad rights.
5. **Gate E — Energy/transport bench.** On development hardware, compare USB power, buffer-assisted MCU burst, and optional solar/hand-generator input. Simulate satellite first; only then evaluate certified hardware and subscriptions.
6. **Gate F — Mechanical/RF feasibility.** Verify candidate module dimensions, antenna ground planes/coexistence, enclosure temperatures, serviceability and regulatory strategy. Only then consider custom carrier/PCB.
7. **Gate G — Field/user study.** Test city, low-data, offline and power-constrained environments; include accessible/non-AI paths. Record what actually succeeded, failed and required another human or institution.

### Measures worth recording

- cold start and wake latency; joules per authenticated message; sustained and burst supply current;
- relay success/retry/duplicate handling; transport switch preserving intent without preserving unjustified trust;
- STOP latency, revoked-action failures, unauthorized-request rejection and graceful brownout behavior;
- physical serviceability, module removal effects, visible mode legibility and accessibility;
- *first safe useful outcome* and time/number of dependencies under zero-possession simulations.

**No real bank funds, passwords, recovery codes or privileged production systems should be exercised in early prototypes.**

## Placement and review strategy

- Keep this proposal at **docs/proposals/COHERENT-RELMOTE-VNEXT.md** and link it from the documentation map.
- Continue with [README](../../README.md) / [STATUS](../STATUS.md) / [ROADMAP](../ROADMAP.md) / [DECISIONS](../DECISIONS.md) as authoritative for present commitments and implemented capabilities.
- Put eventual approved hardware electrical specs under **spec/** and **hardware/** only after validation; put tests/results with the existing bench/validation records.
- Use a private linked knowledge workspace for cross-project idea provenance and planning; **do not mirror sensitive materials into GitHub**.
- This PR should remain **draft** pending review. It does not reprioritize the active Linux software preview or merge paused implementation tracks.
