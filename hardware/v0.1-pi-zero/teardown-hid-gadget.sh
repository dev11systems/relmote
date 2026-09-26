#!/usr/bin/env bash
set -euo pipefail

G=/sys/kernel/config/usb_gadget/relmote

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root." >&2
  exit 1
fi

if [[ ! -d "$G" ]]; then
  echo "Relmote gadget is not configured."
  exit 0
fi

cd "$G"

if [[ -e UDC ]]; then
  echo "" > UDC
fi

rm -f configs/c.1/hid.usb0
rmdir functions/hid.usb0 2>/dev/null || true
rmdir configs/c.1/strings/0x409 2>/dev/null || true
rmdir configs/c.1 2>/dev/null || true
rmdir strings/0x409 2>/dev/null || true
cd /
rmdir "$G" 2>/dev/null || true

echo "Relmote HID gadget removed."
