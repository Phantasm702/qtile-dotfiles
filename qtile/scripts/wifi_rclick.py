#!/bin/python
import multiprocessing
import time

wifi_list_cmd = "nmcli -m tabular -t -f SSID,BARS device wifi"
def get_wifi_list():
    while True:
        wifi_list = subprocess.check_output(wifi_list_cmd, shell=True).decode().split("\n")
        time.sleep(2)



