from core.models import Zarinpal


class ZarinpalConfig:
    def __init__(self):
        self.sandbox = Zarinpal.get_instance().sandbox
        self.merchant_id = Zarinpal.get_instance().merchant_id
        self.access_token = Zarinpal.get_instance().token
