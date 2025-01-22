#!/bin/bash


if [ "$EUID" -ne 0 ]; then
  echo "Veuillez exécuter ce script en tant que root."
  exit 1
fi


airmon-ng start wlan0

airodump-ng wlan0mon -w capture --output-format csv
