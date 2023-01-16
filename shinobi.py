from config_helper import Config
import requests

class Shinobi:
    def __init__(self) -> None:
        config = Config()
        config_shinobi = config.get_config('shinobi')
        self.token = config_shinobi['token']
        self.url = config_shinobi['url']
        self.endpoint = config_shinobi['endpoint']

    def ativar(self):
        self.request("Notification_On")

    def desativar(self):
        self.request("Notification_Off")

    def request(self, preset):
        requests.get(f'{self.url}{self.token}{self.endpoint}{preset}')