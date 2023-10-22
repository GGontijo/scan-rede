import json
from sys import platform
import os

class Config:
    '''Singleton approach'''

    _instance = None

    def __init__(self) -> None:
        if platform == 'linux':
            CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'scan-rede', 'config.json')
        else:
            CONFIG_PATH = 'config.json'
        with open(CONFIG_PATH, 'r') as config:
            self.__config = json.load(config)
        
    def get_config(self, var: str) -> str:
        value = self.__config[var]
        return value

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance