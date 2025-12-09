from django.db import models
from utiles.convert_to_webp import convert_to_webp
import os

def validate_favicon(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.ico':
        raise ValidationError('فایکون باید با پسوند .ico باشد')

    if value.size > 1024 * 1024: 
        raise ValidationError('حجم فایل فایکون نباید بیشتر از 1 مگابایت باشد')

class SiteSettings(models.Model):
    url = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enamad = models.CharField(max_length=1000, blank=True, null=True)
    telegram = models.CharField(max_length=1000, blank=True, null=True)
    instagram = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=1000, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='media/logo/')
    favicon = models.FileField(upload_to='media/favicon/', validators=[validate_favicon])
    contact_us = models.TextField(blank=True, null=True)
    contact_us_image = models.ImageField(upload_to='media/contact_us_image/', blank=True, null=True)
    clarity_tracking_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="شناسه ردیابی Clarity",
        help_text="شناسه ردیابی Microsoft Clarity رو اینجا وارد کنید (مثل qgw9n7vv32)"
    )
    umami_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="شناسه ردیابی Umami",
        help_text="شناسه ردیابی Umami رو اینجا وارد کنید (مثل 1234567890)"
    )
    goftino_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="شناسه گفتینو",
        help_text="شناسه گفتینو رو اینجا وارد کنید (مثل 1234567890)"
    )
    google_tag_manager_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="شناسه ردیابی Google Tag Manager",
        help_text="شناسه ردیابی Google Tag Manager رو اینجا وارد کنید (مثل GTM-TDLFKPTP)"
    )
    def __str__(self):
        return self.meta_title
    def save(self, *args, **kwargs):
        self.pk = 1 
        if self.logo:
            self.logo = convert_to_webp(self.logo.path)
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'