from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import uuid
from utiles.storage import MinioStorage

def generate_referral_code():
    return str(uuid.uuid4())[:6].lower()

class Otp(models.Model):
    otp = models.CharField(max_length=6, verbose_name='کد تایید')
    mobile = models.CharField(max_length=11, verbose_name='شماره موبایل')
    is_used = models.BooleanField(default=False, verbose_name='استفاده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return str(self.otp) + ' - ' + self.mobile
    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=1)


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    avatar = models.ImageField(upload_to='media/avatar/', default='media/avatar/default.png', verbose_name='تصویر آواتار', storage=MinioStorage())
    gender = models.CharField(max_length=10, choices=[('male', 'مرد'), ('female', 'زن')], default='male', verbose_name='جنسیت')
    referral_code = models.CharField(max_length=6, unique=True, default=generate_referral_code, verbose_name='کد معرف')
    invite_code = models.CharField(max_length=6, null=True, blank=True, verbose_name='کد معرفی کننده')
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
    )
    def save(self, *args, **kwargs):
        if not self.referral_code:  # اگه کد معرف نداشت، بساز
            while True:
                code = generate_referral_code()
                if not User.objects.filter(referral_code=code).exists():
                    self.referral_code = code
                    break
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="کاربر")
    title = models.CharField(max_length=100, verbose_name="عنوان آدرس")
    city = models.CharField(max_length=200, verbose_name="شهر")
    province = models.CharField(max_length=200, verbose_name="استان")
    full_address = models.TextField(verbose_name="آدرس کامل")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    is_default = models.BooleanField(default=False, verbose_name="آدرس پیش‌فرض")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
    
    
    

