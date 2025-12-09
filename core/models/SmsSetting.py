from django.db import models

class SmsSetting(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام کاربری')
    password = models.CharField(max_length=255, null=True, blank=True, verbose_name='رمزعبور')
    otp_id= models.CharField(max_length=255, null=True, blank=True, verbose_name='کد الگوی ارسال کد تایید')
    new_order_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='کد الگوی سفارش جدید')
    def save(self, *args, **kwargs):
        self.pk = 1  # همیشه رکورد اول را ذخیره می‌کند
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات سامانه پیامک - ملی پیامک"

    class Meta:
        verbose_name = 'تنظیمات سامانه پیامک'
        verbose_name_plural = 'تنظیمات سامانه پیامک'