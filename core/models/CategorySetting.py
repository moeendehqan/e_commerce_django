from django.db import models
from .service import TelegramService



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