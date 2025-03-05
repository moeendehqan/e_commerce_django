from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, verbose_name='اسلاگ')
    meta_title = models.CharField(max_length=200, verbose_name='عنوان متا')
    meta_description = models.TextField(verbose_name='توضیحات متا')
    meta_keywords = models.TextField(verbose_name='کلمات کلیدی')
    content = RichTextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='media/blog/', null=True, blank=True, verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ‌ها'

