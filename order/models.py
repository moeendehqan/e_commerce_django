from django.db import models
from user.models import User, Address
from product.models import Product, Variant


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets', null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='baskets')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.product.name} - {self.variant.name}"



# Create your models here.
class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'درحال پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'پرداخت ناموفق'),
        ('refunded', 'بازگشت وجه'),
        ('canceled', 'لغو شده'),
    ]
    payment_status = models.CharField(max_length=200, choices=PAYMENT_STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=[('pending', 'درحال پیشنهاد'), ('accepted', 'تایید شده'), ('rejected', 'رد شده'), ('completed', 'تکمیل شده')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.variant.name}"



