from django.db import models
from utiles.convert_to_webp import convert_to_webp
from utiles.storage import MinioStorage


class Slider(models.Model):
    alt = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(upload_to='media/sliders/', verbose_name='تصویر', storage=MinioStorage())
    link = models.URLField(blank=True, null=True, verbose_name='لینک')
    active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return self.alt
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            webp_path = convert_to_webp(self, 'image')
            if webp_path:
                self.image.name = webp_path
                super().save(update_fields=['image'])
    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'