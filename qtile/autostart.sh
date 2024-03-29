#!/bin/bash

## COMMANDS THAT SHOULD ONLY HAVE 1 INSTANCE
# format: <process-name>#<command/path-to-script>
# this is mainly because flatpak apps dont create processes named after the command, for example com.brave.Browser 
# can only be pgrepped with "Brave", and I dont want multiple instances of it running.

cmds=("light-locker#light-locker --lock-on-suspend --lock-on-lid" "picom#picom" "optimus-manager-qt#optimus-manager-qt" "update_checker.py#${HOME}/.config/qtile/scripts/update_checker.py" "firefox#firefox""alacritty#alacritty" "wallpaper_dimmer#${HOME}/.config/qtile/scripts/wallpaper_dimmer" "mpris-proxy#mpris-proxy")

for cmd in "${cmds[@]}";

do
	IFS='#' read -r -a tmp <<< "$cmd"
	if pgrep "${tmp[0]}"; then
		echo "$cmd is already running"
	else
		echo "${tmp[1]} not running"
		eval " ${tmp[1]} &"
    fi
done


## COMMANDS THAT CAN HAVE MULTIPLE INSTANCES/COMMANDS THAT CANT BE PGREPPED
wal -i background.jpg &
export LC_ALL=en_US.UTF-8
nitrogen --set-auto ${HOME}/.config/qtile/background.jpg    # Wallpaper setter
