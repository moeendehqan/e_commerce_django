from django.db import models
from django.utils.text import slugify


class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='media/category/', null=True, blank=True)
    description = models.TextField()
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/product/', null=True, blank=True)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    real_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    discount_percentage = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='variants', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='variants', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.real_price > self.price:
            self.real_price = self.price
            self.discount_percentage = 0
        else:
            self.discount_percentage = ((self.price - self.real_price) / self.price) * 100
        super().save(*args, **kwargs)

    


class VariantImage(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/variant_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.variant.name


