#!/bin/bash

picom --experimental-backends --backend glx &    # Compositor
wal -R &    # Pywal
nitrogen --set-auto background.jpg &    # Wallpaper setter
export LC_ALL=en_US.UTF-8
optimus-manager-qt &    # Nvidia optimus manager systray icon
${HOME}/.config/qtile/scripts/update_checker.py & # Run check updates every 10 minutes
jamesdsp -t &
amixer -q sset Master 15% &
