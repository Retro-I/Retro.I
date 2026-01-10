#!/bin/bash

plymouth_shutdown_file="/usr/lib/systemd/system/plymouth-poweroff.service"
replacement="--mode=reboot"

default_source="$RETROI_DIR/assets/splashscreen/splash.png"
SOURCE="${1:-$default_source}"
TARGET="/usr/share/plymouth/themes/pix/splash.png"

sudo cp -rf "$SOURCE" "$TARGET"
sudo update-initramfs -u

sudo sed -i "s/--mode=shutdown/$replacement/" "$plymouth_shutdown_file" > /dev/null 2>&1

if ! grep -- "$replacement" "$plymouth_shutdown_file"; then
  echo "Shutdown-Bild konnte nicht ausgetauscht werden!" >&2
  exit 1
fi
