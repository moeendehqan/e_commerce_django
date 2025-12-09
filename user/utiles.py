from utiles.melipayamak import Api
from core.models import SmsSetting, SiteSettings



class SendSms:
    def __init__(self) -> None:
        self.setting = SmsSetting.objects.first()
        self.username = self.setting.username
        self.password = self.setting.password
        self.api = Api(self.username, self.password)
        self.bodyIdOtp = self.setting.otp_id
        self.bodyIdNewOrder = self.setting.new_order_id
        self.sms_soap = self.api.sms('soap')
    def send_otp(self, mobile, otp):
        text = [otp]
        self.sms_soap.send_by_base_number(text, mobile, self.bodyIdOtp)
    def send_new_order(self, user, value):
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            return
        if not site_settings.mobile:
            return
        full_name = f"{user.first_name} {user.last_name}"
        text = [full_name, value]
        self.sms_soap.send_by_base_number(text, site_settings.mobile, self.bodyIdNewOrder)


