from django.contrib.sitemaps import Sitemap
from .models import Product, Category



class ProductSitemap(Sitemap):
    changefreq = "daily"  # فرکانس تغییر (مثلاً روزانه)
    priority = 0.9        # اولویت (بین 0 تا 1)

    def items(self):
        # چه اشیایی تو نقشه سایت باشن
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        # آخرین زمان تغییر شیء
        return obj.updated_at

    def location(self, obj):
        # آدرس URL هر شیء
        return obj.get_absolute_url()
    

class CategorySitemap(Sitemap):
    changefreq = "weekly"  # فرکانس تغییر (مثلاً روزانه)
    priority = 0.8        # اولویت (بین 0 تا 1)

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


