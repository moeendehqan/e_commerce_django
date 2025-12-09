from django.db import models
import os
from django.core.exceptions import ValidationError
from .service import TelegramService

def validate_favicon(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.ico':
        raise ValidationError('فایکون باید با پسوند .ico باشد')

    if value.size > 1024 * 1024: 
        raise ValidationError('حجم فایل فایکون نباید بیشتر از 1 مگابایت باشد')



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


class Slider(models.Model):
    alt = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(upload_to='media/sliders/', verbose_name='تصویر')
    link = models.URLField(blank=True, null=True, verbose_name='لینک')
    active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return self.alt
    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

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
    about_us = models.TextField(blank=True, null=True)
    about_us_image = models.ImageField(upload_to='media/about_us_image/', blank=True, null=True)
    telegram_bot = models.CharField(max_length=1000, blank=True, null=True)
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
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

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

class HomeOption(models.Model):
    slider = models.BooleanField(default=True, verbose_name='نمایش اسلایدر')
    best_viewed = models.BooleanField(default=True, verbose_name='نمایش پربازدیدها')
    best_viewed_count = models.IntegerField(default=4, verbose_name='تعداد پربازدیدها')
    new_products = models.BooleanField(default=True, verbose_name='نمایش محصولات جدید')
    new_products_count = models.IntegerField(default=4, verbose_name='تعداد محصولات جدید')
    best_sellers = models.BooleanField(default=True, verbose_name='نمایش پرفروش‌ها')
    best_sellers_count = models.IntegerField(default=4, verbose_name='تعداد پرفروش‌ها')
    offers = models.BooleanField(default=True, verbose_name='نمایش پر تخفیف‌ها')
    offers_count = models.IntegerField(default=4, verbose_name='تعداد پر تخفیف‌ها')
    random_products = models.BooleanField(default=True, verbose_name='نمایش محصولات تصادفی')
    random_products_count = models.IntegerField(default=4, verbose_name='تعداد محصولات تصادفی')

    def save(self, *args, **kwargs):
        self.pk = 1  # همیشه رکورد اول را ذخیره می‌کند
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات صفحه‌ی اصلی"

    class Meta:
        verbose_name = 'تنظیمات صفحه اصلی'
        verbose_name_plural = 'تنظیمات صفحه اصلی'


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


class Zarinpal(models.Model):
    merchant_id = models.CharField(max_length=255,null=True,blank=True)
    token = models.TextField(null=True, blank=True)
    sandbox = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات زرین پال"

    class Meta:
        verbose_name = 'تنظیمات زرین پال'
        verbose_name_plural = 'تنظیمات زرین پال'



class CategorySetting(models.Model):
    title_categories_page = models.CharField(max_length=255, default='دسته بندی', verbose_name='عنوان صفحه دسته بندی')
    CHOICES_CATEGORIES_PAGE= [
        ('classic', ' کلاسیک'),
        ('vertical', ' عمودی'),
    ]
    theme_categories_page = models.CharField(max_length=255, choices=CHOICES_CATEGORIES_PAGE, default='classic', verbose_name='تم صفحه دسته بندی')
    CHOICES_CATEGORIES_HOME= [
        ('story', ' استوری'),
        ('None', ' عدم نمایش'),
        ('square', ' مربع'),
    ]
    theme_categories_home = models.CharField(max_length=255, choices=CHOICES_CATEGORIES_HOME, default='story', verbose_name='تم دست بندی در خانه')
    class Meta:
        verbose_name = 'تنظیمات دسته بندی'
        verbose_name_plural = 'تنظیمات دسته بندی'
    def __str__(self):
        return 'تنظیمات دسته بندی'
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj



