from django.db import models




class Zarinpal(models.Model):
    merchant_id = models.CharField(max_length=255,null=True,blank=True)
    token = models.TextField(null=True, blank=True)
    sandbox = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "تنظیمات زرین پال"

    class Meta:
        verbose_name = 'تنظیمات زرین پال'
        verbose_name_plural = 'تنظیمات زرین پال'

