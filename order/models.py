from django.db import models
from user.models import User, Address
from product.models import Product, Variant
from django.core.validators import MinValueValidator
import uuid
from .telegram import TelegramService
from core.models import TelegramSetting


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets', null=True, blank=True, verbose_name='کاربر')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='baskets', verbose_name='تنوع محصول')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='تعداد')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return f"{self.variant.product.name} - {self.variant}"
    class Meta:
        unique_together = ('user', 'variant')
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='کاربر')
    amount = models.IntegerField(verbose_name='مبلغ')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='توضیحات')    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    fee = models.IntegerField(default=0, verbose_name='کارمزد پرداختیار')
    authority = models.CharField(max_length=255, null=True, blank=True, verbose_name='شناسه یکتای پرداخت')
    STATUS_CHOICES = [
        ('create', 'ایجاد'),
        ('create error', 'خطا در ایجاد'),
        ('pending', 'درحال پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'پرداخت ناموفق'),
        ('refunded', 'بازگشت وجه'),
        ('canceled', 'لغو شده'),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='create', verbose_name='وضعیت')
    ref_id = models.CharField(max_length=200, null=True, blank=True, verbose_name='شناسه پیگیری')
    card_pan = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره کارت')
    card_hash = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره کارت هش شده')
    shaparak_fee = models.IntegerField(default=0, verbose_name='کارمزد شاپرک')
    code = models.CharField(max_length=200, null=True, blank=True, verbose_name='کد وضعیت')
    error_message = models.CharField(max_length=255, null=True, blank=True, verbose_name='پیام خطا')
    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'

class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='orders', verbose_name='پرداخت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    order_number = models.CharField(max_length=200, verbose_name='شناسه سفارش')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    STATUS_CHOICES = [
        ('pending', 'درحال بررسی'),
        ('accepted', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('completed', 'تکمیل شده'),
        ('sent', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'لغو شده'),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', verbose_name='آدرس')
    shipping_cost = models.IntegerField(default=0, verbose_name="هزینه ارسال")
    total_price = models.IntegerField(verbose_name="قیمت کل")
    tracking_code = models.CharField(max_length=200, null=True, blank=True, verbose_name='کد پیگیری')

    def __str__(self):
        return self.order_number
    
    def send_telegram_notification(self):
        telegram_setting = TelegramSetting.get_instance()
        if not telegram_setting.notification_new_order:
            return
        message = f"سفارش جدید:\n"
        message += f"شناسه سفارش: {self.order_number}\n"
        message += f"کاربر: {self.user.username}\n"
        message += f"مبلغ کل: {self.total_price} تومان\n"
        message += f"آدرس: {self.address}\n"
        message += f"وضعیت: {self.status}"
        telegram_service = TelegramService()
        telegram_service.send_message(message)


    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
        self.send_telegram_notification()
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='محصول')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='order_items', verbose_name='تنوع محصول')
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='تعداد')
    subtotal = models.IntegerField(default=0, verbose_name="زیرمجموعه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def save(self, *args, **kwargs):
        self.subtotal = self.variant.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} - {self.variant}"
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'



