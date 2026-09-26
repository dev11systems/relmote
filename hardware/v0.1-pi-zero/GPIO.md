# GPIO backend

The Relmote safety/control semantics do not depend directly on a Raspberry Pi GPIO library.

`PhysicalControls` uses a four-method backend:

```text
setup_input_pullup(pin)
setup_output(pin)
read(pin)
write(pin, value)
```

## gpiozero adapter

The repository includes an optional `GpioZeroBackend`.

Install the Pi extra:

```bash
python -m pip install -e ".[pi,test]"
```

This keeps Raspberry-Pi-specific packages out of normal Relmote installations and CI.

## Why an adapter?

Linux GPIO interfaces and recommended libraries evolve.

The hardware semantics we care about are stable:

- AUTHORIZE is active-low;
- STOP is active-low;
- ARMED is output;
- ACTIVITY is output.

If a future Pi OS favors a different GPIO backend, implement the same tiny interface rather than rewriting safety logic.

## Production Pocket

Production Pocket will not use this Pi adapter. Physical controls will terminate at the independent safety MCU.
