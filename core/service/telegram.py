from .models import TelegramSetting
import requests



class TelegramService:
    def __init__(self):
        self.telegram_setting = TelegramSetting.get_instance()
        self.token = self.telegram_setting.token
        self.chat_ids = self.telegram_setting.chat_id.split(',')
        self.chat_ids = [chat_id.strip() for chat_id in self.chat_ids]
    def send_message(self, message: str):
        for chat_id in self.chat_ids:
            self.send_message_to_chat_id(chat_id, message)
        return True
    def send_message_to_chat_id(self, chat_id: str, message: str):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        data = {
            'chat_id': chat_id,
            'text': message,
        }
        response = requests.post(url, json=data)
        return response.json() 
