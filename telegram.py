import requests
from config_helper import Config

class TelegramBot:
    
    def __init__(self) -> None:
        config = Config()
        config_telegram = config.get_config('telegram')
        self.url = config_telegram['url']
        self.token = config_telegram['token']
        self.chatIds = config_telegram['chatIds']

    def notificar(self, message: str) -> None:
        '''Função que envia as mensagens pelo Telegram.
        >>> Para receber mensagem: https://api.telegram.org/botTOKEN/getUpdates?timeout=100
        '''
        for target in self.chatIds:
            chat_id = target['chatid']
            requests.get(f'{self.url}{self.token}/sendMessage?chat_id={chat_id}&text={message}')