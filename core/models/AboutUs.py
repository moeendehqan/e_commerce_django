from django.db import models
from product.utiles import convert_to_webp



class AboutUs(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    subtitle = models.CharField(max_length=200, verbose_name="زیرعنوان")
    title_content = models.TextField(verbose_name="محتوا عنوان")
    content = models.TextField(verbose_name="محتوا")
    THEME_CHOICES = [
        ('two_column', ' دو ستونی'),
    ]
    theme = models.CharField(max_length=200, verbose_name="تم صفحه", choices=THEME_CHOICES, default='two_column')
    image = models.ImageField(upload_to='media/about_us_image/', blank=True, null=True, verbose_name="تصویر")
    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.pk = 1 
        if self.image:
            self.image = convert_to_webp(self.image)
        super().save(*args, **kwargs)
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj