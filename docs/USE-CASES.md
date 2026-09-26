# Relmote use-case atlas

Relmote is a general **authorized interface node for computing systems**.

“IT support in a pocket” is one especially legible use case, but the architecture should be tested against many environments.

This atlas is deliberately broad. Inclusion means **architecturally relevant**, not “promised in v1.”

## 1. Personal IT support

### Family/friend support

A person plugs Relmote into a machine they want help with.

```text
remote helper
    ↓ Internet
Relmote
    ↓ USB HID / KVM / serial / SSH
computer
```

The local person grants bounded authority rather than permanently installing remote-management software.

Possible tasks:

- diagnose boot problems;
- inspect network configuration;
- guide OS recovery;
- install/update software with approval;
- collect diagnostics;
- explain what is happening;
- switch to Teach mode so the person performs the repair.

### “No software installed” support

Useful when:

- target is not the owner's normal machine;
- installing an agent is undesirable;
- OS is partially broken;
- disk is read-only;
- admin software cannot be installed;
- support should leave no permanent management agent.

### Personal tech toolkit

Carry one Relmote instead of:

- USB keyboard;
- serial adapter;
- Ethernet dongle;
- diagnostic USB;
- KVM gadget;
- several radio bridges.

Modules determine which tools are physically present.

## 2. Professional IT / help desk

Potential authorized environments:

- deskside support;
- break/fix;
- deployment;
- lab support;
- small-business IT;
- field technician work.

Relmote could provide a consistent interface across machines while preserving per-session approval and logs.

It should complement rather than automatically replace established enterprise management.

## 3. Homelab and self-hosting

A Pocket or docked Relmote can act as a portable console for:

- Proxmox hosts;
- NAS systems;
- routers;
- switches;
- headless Linux;
- home automation servers;
- SBCs.

Possible paths:

```text
SSH
serial
KVM
Redfish
Ethernet
USB
```

A permanently docked Relmote could be reachable remotely while remaining owner-controlled.

## 4. Network infrastructure

Console module:

- UART;
- RS-232;
- RJ45 console;
- USB serial;
- Ethernet.

Use cases:

- router/switch recovery;
- broken management network;
- initial provisioning;
- read-only diagnostics;
- out-of-band access.

A mesh/cellular module could provide an independent controller path when the local network itself is the thing that failed.

## 5. Server / datacenter console

Possible interfaces:

- KVM;
- serial;
- Redfish/BMC;
- SSH;
- Ethernet.

Relmote could choose a native management interface when available and fall back to physical KVM/serial when necessary.

## 6. Boot / firmware / recovery

Because some system transports can work before the OS:

- UEFI/BIOS inspection;
- boot-menu interaction;
- installer/recovery environments;
- disk detection;
- bootloader troubleshooting.

Physical authorization remains required for state-changing actions.

## 7. Embedded development

A Relmote module or DIY implementation could expose:

- UART;
- GPIO;
- I²C;
- SPI;
- SWD/JTAG through explicit development modules;
- USB.

Possible uses:

- development-board console;
- firmware test harness;
- sensor/device debugging;
- automated but bounded hardware tests.

Debug interfaces should remain explicit capabilities rather than silently available privileged paths.

## 8. Makers / electronics bench

Relmote as an open field/bench interface:

- serial terminal;
- USB bridge;
- protocol adapter;
- module test fixture;
- programmable human-interface device;
- hardware status viewer.

The open module standard allows specialized community-built adapters.

## 9. Remote sites

Examples:

- remote cabin;
- community network node;
- weather station;
- field research equipment;
- remote server closet;
- inaccessible rooftop/network cabinet.

Controller paths might include:

- cellular;
- LoRa/mesh;
- satellite gateway;
- intermittent Wi-Fi.

Store-and-forward tasks become especially useful.

## 10. Off-grid / disaster / degraded communications

When normal infrastructure is unavailable:

```text
phone
 ↓ BLE
mesh node
 ↓ LoRa
remote Relmote
 ↓ serial
local computer/network equipment
```

Relmote should degrade toward compact tasks/results instead of assuming broadband.

This is not an emergency-services certification claim; it is an architectural use case for unreliable connectivity.

## 11. Community networks

Possible roles:

- portable maintenance node;
- mesh-router console;
- neighborhood infrastructure support;
- shared equipment diagnostics.

Ownership/authorization must remain explicit when equipment is collectively administered.

## 12. Accessibility / alternate interfaces

Relmote can separate **how a person expresses intent** from **how a computer receives input**.

Potential controllers:

- phone accessibility tools;
- switch interfaces;
- voice interfaces;
- alternative keyboards;
- custom AAC/controller software.

The target may simply see ordinary HID or another standard interface.

Relmote should not require a specific physical interaction style.

## 13. Education

### Learning IT

Teach mode can turn a repair into instruction:

```text
Relmote:
"Open the terminal and run this."

human:
performs action

Relmote:
explains result
```

### Networking / embedded labs

Students can inspect:

- transports;
- serial;
- USB;
- routing;
- power;
- protocol design;
- security boundaries.

Open hardware makes the device itself teachable.

## 14. Digital preservation / retrocomputing

Adapters could bridge modern controllers to older systems through:

- serial;
- PS/2 via module;
- legacy keyboard interfaces;
- Ethernet;
- removable media adapters;
- video capture.

This may be useful when installing modern software on the target is impossible or undesirable.

## 15. Device setup / provisioning

For owned/authorized fleets or labs:

- initial setup;
- repetitive configuration;
- device enrollment;
- test stations;
- manufacturing fixtures.

Relmote's bounded action model and physical authorization can distinguish provisioning from uncontrolled keystroke automation.

## 16. QA / hardware/software testing

A Relmote can provide external black-box interaction:

```text
test runner
   ↓
Relmote
   ↓ HID/KVM/serial
device under test
```

Useful for testing:

- boot flows;
- installers;
- recovery;
- UI sequences;
- physical-device behavior.

Observation provenance helps distinguish actual device output from test interpretation.

## 17. Security research / defensive lab work

On systems the operator is authorized to test:

- validate USB trust boundaries;
- test recovery behavior;
- inspect serial consoles;
- evaluate physical authorization UX;
- exercise fail-closed behavior.

Relmote should not add stealth/persistence features merely to broaden this use case.

## 18. Privacy-conscious remote support

A user may prefer a temporary physical support appliance over:

- permanent remote desktop software;
- cloud-linked endpoint agent;
- giving a support provider an ongoing account.

Possible session:

```text
plug in
pair
grant 30-minute capabilities
receive help
revoke
unplug
```

No permanent target-side management software is required for transports such as HID/KVM.

## 19. Air-gapped / isolated lab systems

Where policy permits an authorized external console:

- local manual control;
- KVM;
- serial;
- offline diagnostics;
- physically carried task/evidence envelopes.

Relmote should never assume that “air-gapped” means authorization to bridge networks. Network bridging must be explicit.

## 20. Mobile field workstation companion

A technician/researcher may carry:

- phone/tablet;
- Relmote Pocket;
- selected modules.

The phone/tablet supplies rich UI and optional AI while Relmote supplies physical/system interfaces.

## 21. Headless appliance rescue

For devices that normally have no display/keyboard:

- firewall appliance;
- NAS;
- home automation controller;
- mini server;
- kiosk;
- embedded Linux appliance.

Relmote can select serial, network, or KVM depending on what survives.

## 22. Temporary out-of-band management

Instead of permanently installing dedicated OOB hardware everywhere:

```text
attach Relmote
perform bounded maintenance
detach Relmote
```

Or leave a Relmote docked only where ongoing OOB access is wanted.

## 23. Relmote-to-Relmote assistance

```text
controller
   ↓
Relmote A
   ↓ changing networks
Relmote B
   ↓
target
```

Possible uses:

- remote field support;
- store-and-forward diagnostics;
- cross-site maintenance;
- constrained network traversal.

Trust remains node- and target-specific.

## 24. Local AI hardware interface

An AI running elsewhere can use Relmote as its **bounded physical/system interface**.

Examples:

- home-server model;
- workstation model;
- phone model;
- cloud model.

The model proposes actions; Relmote supplies policy, capability awareness, physical authorization, and transports.

## 25. Human-only universal console

AI is optional.

A user can operate Relmote as:

- KVM;
- terminal;
- serial console;
- network console;
- transport bridge;
- modular diagnostic tool.

This is important for longevity: Relmote remains useful even if every AI integration is disabled.

# Cross-cutting use-case dimensions

Rather than treating every scenario as a separate product, describe them along common dimensions.

## Controller distance

```text
same device
nearby
same LAN
remote Internet
constrained mesh
intermittent/store-and-forward
```

## Target feedback

```text
none
text
screen
structured API
multiple
```

## Target state

```text
healthy OS
degraded OS
recovery
bootloader
firmware/UEFI
powered off but OOB reachable
```

## Authority

```text
observe
teach
assist
operate
```

plus explicit capabilities.

## Persistence

```text
temporary attached tool
long-lived docked node
embedded Relmote-compatible implementation
```

## Intelligence

```text
human only
deterministic automation
local model
phone model
self-hosted model
cloud model
hybrid
```

# Design test

A new feature should not be justified merely by “another use case.”

Ask:

1. Does it fit the general capability/transport model?
2. Can it remain explicitly authorized?
3. Does it preserve human visibility/control?
4. Can it be implemented as a module/plugin instead of bloating Pocket?
5. Does it improve more than one scenario?
6. Does it create a new trust boundary that needs explicit modeling?

That keeps the use-case atlas expansive without turning Relmote into an incoherent everything-device.
