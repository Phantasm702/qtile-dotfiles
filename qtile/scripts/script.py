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
import sys
from time import sleep

home = os.path.expanduser("~/.config/qtile/scripts/")





#####################
##### BLUETOOTH #####
#####################


bt_info_cmd = "bluetoothctl show"
bt_connected_cmd = "bluetoothctl devices Connected"

bt_on = "\uf294"
bt_off = "\uf5b1"


def get_bt_info():
    
    bt_info = subprocess.check_output(bt_info_cmd, shell=True).decode()
    bt_connected = subprocess.check_output(bt_connected_cmd, shell=True).decode().split()
        
    if "Powered: yes" in bt_info:
        if len(bt_connected) != 0:
            print(bt_on + " " + str(bt_connected[2:]).replace("[", "").replace("'", "").replace(",", "").replace("]", ""))
        else:
            print(bt_on)
    else:
        print(bt_off)





################
##### WIFI #####
################


wifi_on = "\ufaa8"
wifi_off = "\ufaa9"
wifi_state_cmd = "cat /sys/class/net/wlan0/operstate"
ssid_cmd = "iwgetid -r"

def get_wifi_info():
    state = subprocess.check_output(wifi_state_cmd, shell=True).decode().strip()
    
    try:
        ssid = subprocess.check_output(ssid_cmd, shell=True).decode().strip()
    except:
        ssid = ""

#    print(state)

    if state == "up":
#        print("up")
        print(wifi_on + " " + ssid)
    else:
        print(wifi_off)





####################
##### ETHERNET #####
####################


eth = "\uf6ff"
eth_state_cmd = ("cat /sys/class/net/enp2s0/carrier")

def get_eth_info():
    check = subprocess.check_output(eth_state_cmd, shell=True).decode().strip()

    if check == "1":
        print(eth)





###################
##### BATTERY #####
###################


bat_icons = ["\uf579", "\uf57a", "\uf57b", "\uf57c", "\uf57d", "\uf57e", "\uf57f", "\uf580", "\uf581", "\uf578", "\uf583"]
bat_info_cmd = "upower -i /org/freedesktop/UPower/devices/battery_BAT0"
bat_percentage_cmd = 'upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep "percentage"'

def get_bat_info():
    bat_percentage = subprocess.check_output(bat_percentage_cmd, shell=True).decode().strip().split(":          ")[1]
    bat_level = int(bat_percentage.strip("%"))
    current_icon = bat_icons[bat_level//10 - 1]

    bat_info = subprocess.check_output(bat_info_cmd, shell=True).decode()
    if "state:               charging" in bat_info:
        current_icon = bat_icons[10]
    print(current_icon + " " + bat_percentage)






######################
##### WIFI-CLICK #####
######################


wifi_state_cmd = "cat /sys/class/net/wlan0/operstate"
wifi_on_cmd = "nmcli radio wifi on"
wifi_off_cmd = "nmcli radio wifi off"

def wifi_l_click():
    state = subprocess.check_output(wifi_state_cmd, shell=True).decode().strip()

    if state == "up":
        print("turning wifi off...")
        subprocess.call(wifi_off_cmd, shell=True)
    else:
        print("turning wifi on...")
        subprocess.call(wifi_on_cmd, shell=True)





######################
##### BT-CLICK #####
######################


bt_info_cmd = "bluetoothctl show"
bt_connected_cmd = "bluetoothctl devices Connected"

bt_on_cmd = "bluetoothctl power on"
bt_off_cmd = "bluetoothctl power off"

def bt_l_click():

    bt_info = subprocess.check_output(bt_info_cmd, shell=True).decode()
    
    if "Powered: yes" in bt_info:
        state = "up"
    else:
        state = "down"


    if state == "up":
        print("turning bluetooth off...")
        subprocess.call(bt_off_cmd, shell=True)
    else:
        print("turning bluetooth on...")
        subprocess.call(bt_on_cmd, shell=True)


bt_term_cmd = "alacritty -e bluetoothctl"

def bt_r_click():
    subprocess.call(bt_term_cmd, shell=True)







###################
##### PARSING #####
###################


args = sys.argv[1:]

#print(args[0])

if len(args) == 0:
    print("At least one argument is required")

elif args[0] == "bt" or args[0] == "bluetooth":
#    print("Getting bluetooth...")
    get_bt_info()

elif args[0] == "wifi":
#    print("Getting wifi...")
    get_wifi_info()

elif args[0] == "eth" or args[0] == "ethernet":
#    print("Getting ethernet...")
    get_eth_info()

elif args[0] == "bat" or args[0] == "battery":
#    print("Getting battery...")
    get_bat_info()

elif args[0] == "lclick":
    if args[1] == "wifi":
        wifi_l_click()
    elif args[1] == "bt" or args[1] == "bluetooth":
        bt_l_click()

elif args[0] == "rclick":
    if args[1] == "bt" or args[1] == "bluetooth":
        bt_r_click()
else:
    print("Unknown argument '" + args[0] + "'")

