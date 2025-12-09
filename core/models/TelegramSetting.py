from django.db import models

class TelegramSetting(models.Model):
    token = models.CharField(max_length=255, null=True, blank=True, verbose_name='توکن تلگرام')
    notification_new_order = models.BooleanField(default=True, verbose_name='اطلاع رسانی سفارش جدید')
    notification_new_contact = models.BooleanField(default=True, verbose_name='اطلاع رسانی تماس با مای جدید')
    chat_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='آیدی چت تلگرام')
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    def __str__(self):
        return "تنظیمات تلگرام"
    class Meta:
        verbose_name = 'تنظیمات تلگرام'
        verbose_name_plural = 'تنظیمات تلگرام'

