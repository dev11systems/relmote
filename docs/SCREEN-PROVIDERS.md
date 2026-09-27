# Screen providers

Relmote models screen access as a capability supplied by interchangeable providers.

The controller asks for `screen.observe` or, separately, `screen.control`. It should not need to know whether pixels originate from an OS portal, an existing remote-desktop service, a VM console, or physical capture hardware.

## Provider classes

### Wayland portal / PipeWire

- OS-mediated source selection and consent.
- PipeWire supplies the selected video stream.
- Observe does not imply input control.
- Graphical control uses a separate Remote Desktop permission path.

### GNOME Remote Desktop / RDP

A mature GNOME-native provider may be used when already installed/configured and policy permits it. Relmote should discover rather than silently enable persistent remote-desktop services.

### VNC

Existing VNC tooling may be adapted when explicitly configured. Relmote must not silently weaken authentication or expose a VNC listener to an untrusted network.

### X11 native

Use only when the target session is actually X11 and according to active Relmote policy.

### VM/container console

Hypervisor or container console APIs can supply screen/console access without interacting with a physical desktop session.

### Hardware KVM

Relmote hardware can supply video observation and USB HID input independently of the target OS, including firmware, boot loaders, login screens, and OS failures.

## Provider selection

Provider choice is policy, not merely availability. Selection may consider explicit user choice, required capability, consent/security properties, existing configuration, network exposure, target scope, quality/latency, and hardware availability.

Automatic selection must remain visible and reversible.

## Display-topology invariant

`screen.observe` must not intentionally alter the target's physical display topology.

Starting observation must not silently enable/disable displays, switch extended displays to mirroring, change resolution/scale/rotation/primary display, or create a virtual display unless explicitly requested.

When practical, Relmote should record topology before and after provider activation and surface unexpected changes as an attention item. A provider requiring a virtual monitor or topology change must advertise that behavior before activation.