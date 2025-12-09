from django.apps import apps
import requests



class TelegramService:
    def __init__(self):
        TelegramSetting = apps.get_model('core', 'TelegramSetting')
        self.telegram_setting = TelegramSetting.get_instance()
        self.token = (self.telegram_setting.token or '').strip()
        chat_ids_raw = (self.telegram_setting.chat_id or '')
        self.chat_ids = [c.strip() for c in chat_ids_raw.split(',') if c.strip()]
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
