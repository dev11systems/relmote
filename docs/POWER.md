# Power architecture

Relmote should be able to operate from multiple power sources without treating any one source as mandatory.

The power system is part of the platform architecture, not merely a battery choice.

## Desired power sources

A Relmote implementation may accept some combination of:

- USB-C input;
- USB-C Power Delivery;
- internal battery;
- removable battery module;
- target-provided USB power;
- dock power;
- PoE through a module/dock;
- external battery bank;
- external DC/solar module;
- vehicle/field power through an appropriate regulated adapter.

## Core rule

**Power relationship and control authority are separate concepts.**

A target computer powering Relmote must not automatically authorize Relmote to control that target.

Likewise, Relmote providing power to another device must not silently create a data/control path.

## Reference Pocket layout

A reference Pocket Relmote should strongly consider separate ports:

```text
USB-C POWER / CONTROLLER
USB-C TARGET
USB-C EXPANSION   (optional)
```

Separating roles reduces ambiguous power/data behavior and makes physical state easier to understand.

## Battery philosophy

Battery support should be optional at the platform level.

A Relmote should remain useful as:

```text
batteryless core + external USB-C power
```

Pocket and Field reference designs may include batteries.

Reference batteries should be:

- replaceable;
- mechanically accessible without adhesive destruction;
- protected by standard battery-management circuitry;
- independently serviceable from the main board where practical.

The product should accept a few extra millimeters of thickness rather than make the battery effectively non-replaceable.

## Power-path management

A multi-source Relmote needs explicit power-path control.

The design must prevent unintended backfeeding between:

- target USB;
- USB-C input;
- internal battery;
- external battery module;
- dock/module rails.

No connector should become a surprise source merely because another power source is attached.

## Output power

Some Relmote variants may intentionally provide power to external devices, including acting as a small emergency power bank.

If supported, output power must be:

- explicit;
- separately controllable from data/control authorization;
- current-limited;
- visible in status;
- disabled by default on ports where role ambiguity would be dangerous.

## Module power

Snap modules should receive a defined module power rail plus control metadata describing:

- nominal voltage;
- current limit;
- peak allowance;
- startup allowance;
- whether the module can source power;
- whether it can pass power downstream.

A module should never assume unlimited downstream power.

## Power budgeting

Relmote should maintain a runtime power budget.

Example:

```text
available:        12 W
core reserve:      3 W
KVM module:        4 W
LoRa peak reserve: 2 W
downstream free:   3 W
```

If a requested configuration exceeds the budget, the system should refuse or degrade rather than brown out unpredictably.

## Sleep and low-power operation

Relmote should distinguish at least:

- active;
- connected-idle;
- low-power listening;
- store-and-forward standby;
- powered-off but chargeable.

A mesh-only or scheduled store-and-forward Relmote may spend most of its life in low-power state.

## Battery modules

A snap-on battery may extend runtime without changing the Relmote software model.

```text
Relmote Pocket
      ║
   battery module
```

Battery modules should expose state such as:

- state of charge;
- health;
- temperature;
- charge/discharge limits;
- design capacity;
- cycle count when available.

## Docks

A dock may combine:

- charging;
- Ethernet;
- KVM/video;
- serial;
- additional USB;
- external storage.

A dock should enumerate capabilities just like any other module rather than becoming a special-case subsystem.

## Open questions

The reference hardware still needs empirical answers for:

- target-power limits;
- ideal battery chemistry/form factor;
- charging thermals;
- hot-swap behavior;
- batteryless operation during source transitions;
- whether the safety plane requires an independent reserve supply;
- whether STOP should electrically disconnect target data as well as logically revoke output.
