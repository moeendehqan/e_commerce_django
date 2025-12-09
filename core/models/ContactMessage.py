from django.db import models
from core.service import TelegramService
from .TelegramSetting import TelegramSetting



class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده‌شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def send_telegram_notification(self):
        telegram_service = TelegramService()
        message = f"""
        پیام جدید تماس با ما
        نام: {self.name}
        ایمیل: {self.email}
        موضوع: {self.subject}
        پیام: {self.message}
        """
        telegram_service.send_message(message)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        telegram_setting = TelegramSetting.get_instance()
        if telegram_setting.notification_new_contact:
            self.send_telegram_notification()

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"