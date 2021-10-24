#!/bin/bash

cat << 'EOS' | sudo tee -a /etc/udev/rules.d/90-nfc.rules
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="06c3", GROUP="plugdev"
EOS

cat << 'EOS' | sudo tee -a /etc/modprobe.d/blacklist-nfc.conf
blacklist port100
EOS

sudo udevadm control -R
