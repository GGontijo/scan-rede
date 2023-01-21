import subprocess
import os
from telegram import TelegramBot
from sys import platform
import time
import map_hosts
from shinobi import Shinobi
import json
from config_helper import Config


class ScanRede:
    
    def __init__(self) -> None:
        if platform == 'linux':
            self.default_cachefile_path = os.path.join(os.path.expanduser('~'), 'scripts', 'scan-rede', 'cachefile')
            self.default_log_path = os.path.join(os.path.expanduser('~'), 'scripts', 'scan-rede', 'log.txt')
            print(self.default_cachefile_path)
        else:
            self.default_cachefile_path = 'cachefile'
            self.default_log_path = 'log.txt'
        config = Config()
        self.telegram = TelegramBot()
        self.shinobi = Shinobi()
        self.config_parameters = config.get_config('parameters')
        self.known_hosts = self.config_parameters['known_hosts']
        self.ler_status()
        self.scanear_rede()
        self.change_status()

    def change_status(self):
        presence = self.valida_presence()
        horario = self.valida_horario()

        if presence or horario:
            if self.current_status['status'] != True:
                self.current_status['status'] = True
                self.shinobi.ativar()
                self.telegram.notificar("Notificações ativadas!")
        else:
            if self.current_status['status'] != False:
                self.current_status['status'] = False
                self.shinobi.desativar()
                self.telegram.notificar("Notificações desativadas!")
        
        self.gravar_status()

        
    def valida_horario(self) -> bool:
        print(time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S") >= self.config_parameters['time_range']['start'] and time.strftime("%H:%M:%S") <= self.config_parameters['time_range']['end']:
            return True
        
        else:
            return False


    def valida_presence(self) -> bool:
        if self.matches != []:
            self.current_status['presence'] = self.matches
            return False

        else:
            self.current_status['presence'] = self.matches
            return True


    def gravar_status(self):
        json_file = json.dumps(self.current_status, indent=4)

        with open(self.default_cachefile_path, 'w') as file:
            file.write(json_file)

            

    def ler_status(self):
        try:
            with open(self.default_cachefile_path, 'r') as file:
                self.current_status = json.load(file)
        except Exception as e:
            self.default_status()
            with open(self.default_cachefile_path, 'r') as file:
                self.current_status = json.load(file)


    def default_status(self):
        
        status = {
            "presence": [],
            "status": True
        }

        json_file = json.dumps(status, indent=4)

        with open(self.default_cachefile_path, 'w') as file:
            file.write(json_file)


    def scanear_rede(self):
        if platform == 'linux':
            output = subprocess.check_output(self.config_parameters["arp_scan_command"], shell=True)
            self.logger(f'output {output}')
            self.arp_hosts = output.decode().split("\n")
            mapping = map_hosts.MapHosts(self.known_hosts,self.arp_hosts)
            self.matches = mapping.match()
            print(self.matches)
        else:
            self.arp_hosts = []
            mapping = map_hosts.MapHosts(self.known_hosts,self.arp_hosts)
            self.matches = mapping.match()
            print(self.matches)

    def logger(self, message):
        with open(self.default_log_path, 'w') as log:
                log.writelines(message)
            

if __name__ == '__main__':
    ScanRede()
