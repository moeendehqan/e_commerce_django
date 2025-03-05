from melipayamak import Api
from core.models import SiteSettings



class SendSms:
    def __init__(self) -> None:
        self.setting = SiteSettings.objects.first()
        self.username = self.setting.user_melipayamak
        self.password = self.setting.password_melipayamak
        self.api = Api(self.username, self.password)
        self.bodyIdOtp = self.setting.otp_id_melipayamak
        self.sms_soap = self.api.sms('soap')
    def send_otp(self, mobile, otp):
        text = [otp]
        self.sms_soap.send_by_base_number(text, mobile, self.bodyIdOtp)
