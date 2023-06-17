#!/bin/python

# TODO:
# 1) Parse args to detect which output is needed
#  1.1) Check if we can python print icons to status bar instead of shell printf, to get rid of .txt files
#  
# 2) Add bluetooth functionality (*bluetoothctl)
#  2.1) *Check if we can use bluetoothctl in non-interactive mode for use in this script
#
# 3) Combine all scripts into this, next UPDATER.SH
#
# 4) After adding all functionality, rename script to script.py or something more sensible



from multiprocessing import Process
import subprocess
import os
from time import sleep



update_icon = "󰚰"
check_updates_cmd = "checkupdates | wc -l"


def check_updates():
    global updates
    
    print("Fetching updates...")

    try:
        updates = str(subprocess.check_output(check_updates_cmd, shell=True).decode())
    except subprocess.CalledProcessError:
        updates = "0"
    
    while "Cannot fetch updates" in updates:
        print("Cannot fetch updates, retrying...")
        try:
            updates = str(subprocess.check_output(check_updates_cmd, shell=True).decode())
        except subprocess.CalledProcessError:
            updates = "0"


def write_updates():
    while True:
        check_updates()

        final = update_icon + " " + updates.strip(" ").strip("\n")

        with open(os.path.expanduser("~/.config/qtile/scripts/updates.txt"), "w") as f:
            f.write(final)
        sleep(600)


print("****Starting main****")
print("STARTING PROCESS: LOOP WRITE UPDATES")
Process(target=write_updates).start()
