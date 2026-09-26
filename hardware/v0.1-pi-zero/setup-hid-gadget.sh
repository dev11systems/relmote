#!/usr/bin/env bash
set -euo pipefail

# Relmote v0.1 USB HID gadget setup.
#
# Prototype use only. This script assumes the Pi's USB controller is already
# configured for peripheral/OTG mode and that configfs is available.
# It creates one standard boot-protocol keyboard function at /dev/hidg0.
#
# Run only on a Relmote prototype that you own/control.

G=/sys/kernel/config/usb_gadget/relmote

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root." >&2
  exit 1
fi

modprobe libcomposite

if [[ ! -d /sys/kernel/config/usb_gadget ]]; then
  echo "USB gadget configfs is unavailable." >&2
  exit 1
fi

if [[ -e "$G/UDC" ]] && [[ -n "$(cat "$G/UDC" 2>/dev/null || true)" ]]; then
  echo "Relmote gadget is already bound. Unbind it before reconfiguring." >&2
  exit 1
fi

mkdir -p "$G"
cd "$G"

# Prototype IDs only; production hardware needs properly assigned USB identity.
echo 0x1d6b > idVendor
echo 0x0104 > idProduct
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir -p strings/0x409
echo "relmote-prototype" > strings/0x409/serialnumber
echo "Dev11" > strings/0x409/manufacturer
echo "Relmote v0.1 prototype" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Relmote HID" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

# Standard 8-byte USB HID boot-keyboard report descriptor.
printf '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' \
  > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/ 2>/dev/null || true

UDC="$(ls /sys/class/udc | head -n 1)"
if [[ -z "$UDC" ]]; then
  echo "No USB Device Controller found. Verify OTG/peripheral mode first." >&2
  exit 1
fi

echo "$UDC" > UDC

echo "Relmote HID gadget bound to $UDC"
echo "Expected device: /dev/hidg0"
