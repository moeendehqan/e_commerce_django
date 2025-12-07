from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from .utiles import convert_to_webp


class Color(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام رنگ')
    code = models.CharField(max_length=200, verbose_name='کد رنگ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ‌ها'

class Size(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام سایز')
    code = models.CharField(max_length=200, verbose_name='کد سایز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز‌ها'

class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام برند')
    slug = models.SlugField(max_length=200, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='media/brand/', null=True, blank=True, verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    meta_title = models.CharField(max_length=200, verbose_name='عنوان متا')
    meta_description = models.TextField(verbose_name='توضیحات متا')
    meta_keywords = models.TextField(verbose_name='کلمات کلیدی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
    def __str__(self):
        return self.name
    
class ProductAttribute(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام ویژگی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی‌های محصولات'
    def __str__(self):
        return self.name

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=200, verbose_name='اسلاگ')
    image = models.ImageField(upload_to='media/category/', null=True, blank=True, verbose_name='تصویر')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True, blank=True, verbose_name='دسته‌بندی والد')
    description = models.TextField(verbose_name='توضیحات')
    meta_title = models.CharField(max_length=200, verbose_name='عنوان متا')
    meta_description = models.TextField(verbose_name='توضیحات متا')
    meta_keywords = models.TextField(verbose_name='کلمات کلیدی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[self.slug])
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        webp_path = convert_to_webp(self, 'image')
        if webp_path:
            self.image.name = webp_path
            super().save(update_fields=['image'])

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(max_length=200, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='products', null=True, blank=True, verbose_name='برند')
    new = models.BooleanField(default=True, verbose_name='جدید')
    image = models.ImageField(upload_to='media/product/', null=True, blank=True, verbose_name='تصویر')
    meta_title = models.CharField(max_length=200, verbose_name='عنوان متا')
    meta_description = models.TextField(verbose_name='توضیحات متا')
    meta_keywords = models.TextField(verbose_name='کلمات کلیدی')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='دسته‌بندی')
    count_view = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    waranty = models.CharField(max_length=200,null=True, blank=True, verbose_name='گارانتی')
    count_sell = models.IntegerField(default=0, verbose_name='تعداد فروش')
    price = models.IntegerField(verbose_name='قیمت',null=True, blank=True)
    real_price = models.IntegerField(verbose_name='قیمت واقعی',null=True, blank=True)
    discount_percentage = models.IntegerField(default=0, verbose_name='درصد تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        webp_path = convert_to_webp(self, 'image')
        if webp_path:
            self.image.name = webp_path
            super().save(update_fields=['image'])
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', verbose_name='محصول')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values', verbose_name='ویژگی')
    value = models.CharField(max_length=200, verbose_name='مقدار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    class Meta:
        verbose_name = 'مقدار ویژگی محصول'
        verbose_name_plural = 'مقدار ویژگی‌های محصولات'
    def __str__(self):
        return f"{self.product.name} - {self.attribute.name} - {self.value}"

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='محصول')
    price = models.IntegerField(verbose_name='قیمت')
    real_price = models.IntegerField(verbose_name='قیمت واقعی')
    quantity = models.IntegerField(default=1, verbose_name='تعداد')
    discount_percentage = models.IntegerField(default=0, verbose_name='درصد تخفیف')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='variants', null=True, blank=True, verbose_name='رنگ')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='variants', null=True, blank=True, verbose_name='سایز')
    is_default = models.BooleanField(default=False, verbose_name='پیش‌فرض')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        name = self.product.name
        if self.color:
            name += ' - ' + self.color.name
        if self.size:
            name += ' - ' + self.size.name
        return name
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Variant.objects.filter(product=self.product).update(is_default=False)
        if Variant.objects.filter(product=self.product, is_default=True).count() == 0:
            self.is_default = True
        if self.real_price > self.price:
            self.real_price = self.price
            self.discount_percentage = 0
        else:
            self.discount_percentage = ((self.price - self.real_price) / self.price) * 100
        if self.is_default:
            self.product.price = self.price
            self.product.real_price = self.real_price
            self.product.discount_percentage = self.discount_percentage
            self.product.save()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'تنوع'
        verbose_name_plural = 'تنوع‌ها'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = models.ImageField(upload_to='media/product_images/', null=True, blank=True, verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        webp_path = convert_to_webp(self, 'image')
        if webp_path:
            self.image.name = webp_path
            super().save(update_fields=['image'])
