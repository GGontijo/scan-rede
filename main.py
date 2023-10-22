import subprocess
import os
from telegram import TelegramBot
from sys import platform
import time
from map_hosts import MapHosts
from shinobi import Shinobi
import json
from config_helper import Config
from datetime import datetime


class ScanRede:
    
    def __init__(self) -> None:
        if platform == 'linux':
            self.default_cachefile_path = os.path.join(os.path.expanduser('~'), 'scan-rede', 'cachefile')
            self.default_log_path = os.path.join(os.path.expanduser('~'), 'scan-rede', 'log.txt')
            self.logger(self.default_cachefile_path)
            self.logger(self.default_log_path)
        else:
            self.default_cachefile_path = 'cachefile'
            self.default_log_path = 'log.txt'
        config = Config()
        self.telegram = TelegramBot()
        self.shinobi = Shinobi()
        self.config_parameters = config.get_config('parameters')
        self.known_hosts = self.config_parameters['known_hosts']
        self.watch_dog_hosts = self.config_parameters['watch_dog_hosts']
        self.mapping = MapHosts(self.known_hosts)
        self.ler_status()
        self.scanear_rede()
        self.monitorar_dispositivo()
        self.change_status()
        

    def change_status(self):
        presence = self.valida_presence()
        horario = self.valida_horario()
        event_person = []

        if presence or horario:
            if self.current_status['status'] != True:
                self.current_status['status'] = True
                for k in self.map:
                    if self.map[k]["action"] == "Saiu":
                        event_person.append(k)
                self.shinobi.ativar()
                self.telegram.notificar(f"Notificações ativadas, {' '.join(map(str, event_person))} Saiu!")
        else:
            if self.current_status['status'] != False:
                self.current_status['status'] = False
                for k in self.map:
                    if self.map[k]["action"] == "Entrou":
                        event_person.append(k)
                self.shinobi.desativar()
                self.telegram.notificar(f"Notificações desativadas, {' '.join(map(str, event_person))} Entrou!")
        
        self.gravar_status()

        
    def valida_horario(self) -> bool:
        self.logger(time.strftime("%H:%M:%S"))
        if time.strftime("%H:%M:%S") >= self.config_parameters['time_range']['start'] and time.strftime("%H:%M:%S") <= self.config_parameters['time_range']['end']:
            return True
        else:
            return False


    def valida_presence(self) -> bool:
        self.current_presence_list = []
        if self.map != []:
            for k in self.map:
                if self.map[k]["action"] != "Saiu":
                    self.current_presence_list.append(k)
            if self.current_presence_list != []:
                self.current_status['presence'] = self.current_presence_list
                return False
            else: 
                self.current_status['presence'] = self.current_presence_list
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
            self.logger(e)
            self.default_status()
            with open(self.default_cachefile_path, 'r') as file:
                self.current_status = json.load(file)


    def default_status(self):
        self.logger("cachefile não encontrado! gerando um a partir do modelo...")
        status = {
            "presence": [],
            "status": True,
            "host_inoperante": False
        }

        json_file = json.dumps(status, indent=4)

        with open(self.default_cachefile_path, 'w') as file:
            file.write(json_file)


    def scanear_rede(self):
        if platform == 'linux':
            output = subprocess.getoutput(self.config_parameters["arp_scan_command"])
            self.logger(output)
            self.arp_hosts = output.split("\n")
            self.logger(self.arp_hosts)
            self.map = self.mapping.match(self.arp_hosts, self.current_status['presence'])
            self.logger(self.map)
        else:
            self.arp_hosts = ["0c:cb:85:36:c6:39"]
            self.map = self.mapping.match(self.arp_hosts, self.current_status['presence'])
            self.logger(self.map)
    
    def monitorar_dispositivo(self):
        '''Monitora dispositivo na rede, está feito para apenas um dispositivo, ajustar antes de usar com mais'''

        for host in self.watch_dog_hosts:
            for k, v in host.items():
                if v not in self.arp_hosts and not self.current_status['host_inoperante']:
                    self.telegram.notificar(f'Dispositivo {k} não foi encontrado na rede!')
                    self.current_status['host_inoperante'] = True # Evita notificar a cada intervalo
                if v in self.arp_hosts and self.current_status['host_inoperante']:
                    self.telegram.notificar(f'Dispositivo {k} encontrado novamente!')
                    self.current_status['host_inoperante'] = False # Evita notificar a cada intervalo

    def logger(self, message):
        print(message)
        with open(self.default_log_path, 'a') as log:
            log.writelines(f"{datetime.now()}: {str(message)}\n")
            

if __name__ == '__main__':
    ScanRede()
