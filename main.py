import subprocess
from sys import platform
import os
import json
from config_helper import Config


class ScanRede:
    
    def __init__(self) -> None:
        config = Config()
        self.config_parameters = config.get_config('parameters')
        self.config_telegram = config.get_config('telegram')
        self.config_shinobi = config.get_config('shinobi')
        self.ler_status()
        self.scanear_rede()

    
    def ler_status(self):
        try:
            with open('cachefile', 'r') as file:
                self.current_status = json.load(file)
        except:
            self.default_status()
            with open('cachefile', 'r') as file:
                self.current_status = json.load(file)


    def default_status(self):
        status = {
            "presence": [],
            "status": True
        }

        json_file = json.dumps(status, indent=4)

        with open('cachefile', 'w') as file:
            file.write(json_file)


    def scanear_rede(self):
        if platform != 'linux':
            output = subprocess.getoutput(self.config_parameters["arp_scan_command"])
            print(output)

if __name__ == '__main__':
    ScanRede()
