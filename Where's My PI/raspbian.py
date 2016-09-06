__author__ = '13123935 - Jordan Harman'
import subprocess
import json


def get_details():
    data = {
        "temperature":
            subprocess.Popen(["/opt/vc/bin/vcgencmd", "measure_temp"], stdout=subprocess.PIPE).communicate()[
                0].replace("temp=", "").replace("\n", ""),
        "hostname": subprocess.Popen(["hostname"], stdout=subprocess.PIPE).communicate()[0].replace("\n", ""),
        "username": "pi",
        "password": "raspberry",
        "powerstate": "online"
    }
    return json.dumps(data)

def shutdown_details():
    data = {
        "temperature": "N/A",
        "hostname": subprocess.Popen(["hostname"], stdout=subprocess.PIPE).communicate()[0].replace("\n", ""),
        "username": "pi",
        "password": "raspberry",
        "powerstate": "offline"
    }
    return json.dumps(data)

def shutdown():
    shuttingdown = subprocess.Popen(["sudo shutdown"], stdout=subprocess.PIPE).communicate()[0]

def reboot_details():
    data = {
        "temperature": "N/A",
        "hostname": subprocess.Popen(["hostname"], stdout=subprocess.PIPE).communicate()[0].replace("\n", ""),
        "username": "pi",
        "password": "raspberry",
        "powerstate": "restarting"
    }
    return json.dumps(data)

def reboot():
    shuttingdown = subprocess.Popen(["sudo reboot"], stdout=subprocess.PIPE).communicate()[0]