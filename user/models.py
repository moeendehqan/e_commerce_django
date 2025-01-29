from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

class Otp(models.Model):
    otp = models.CharField(max_length=6)
    mobile = models.CharField(max_length=11)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.otp


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    avatar = models.ImageField(upload_to='media/avatar/', default='media/avatar/default.png')
    gender = models.CharField(max_length=10, choices=[('male', 'مرد'), ('female', 'زن')], default='male')
    referral_code = models.CharField(max_length=6, unique=True)
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
    def __str__(self):
        return self.username
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    invoice_address = models.BooleanField(default=False)
    delivery_address = models.BooleanField(default=False)
    city = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.address
    
    
    
    

