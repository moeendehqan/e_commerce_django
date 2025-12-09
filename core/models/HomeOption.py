from django.db import models




class HomeOption(models.Model):
    slider = models.BooleanField(default=True, verbose_name='نمایش اسلایدر')
    best_viewed = models.BooleanField(default=True, verbose_name='نمایش پربازدیدها')
    best_viewed_count = models.IntegerField(default=4, verbose_name='تعداد پربازدیدها')
    new_products = models.BooleanField(default=True, verbose_name='نمایش محصولات جدید')
    new_products_count = models.IntegerField(default=4, verbose_name='تعداد محصولات جدید')
    best_sellers = models.BooleanField(default=True, verbose_name='نمایش پرفروش‌ها')
    best_sellers_count = models.IntegerField(default=4, verbose_name='تعداد پرفروش‌ها')
    offers = models.BooleanField(default=True, verbose_name='نمایش پر تخفیف‌ها')
    offers_count = models.IntegerField(default=4, verbose_name='تعداد پر تخفیف‌ها')
    random_products = models.BooleanField(default=True, verbose_name='نمایش محصولات تصادفی')
    random_products_count = models.IntegerField(default=4, verbose_name='تعداد محصولات تصادفی')

    def save(self, *args, **kwargs):
        self.pk = 1  # همیشه رکورد اول را ذخیره می‌کند
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات صفحه‌ی اصلی"

    class Meta:
        verbose_name = 'تنظیمات صفحه اصلی'
        verbose_name_plural = 'تنظیمات صفحه اصلی'