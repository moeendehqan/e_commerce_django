from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product.sitemaps import ProductSitemap, CategorySitemap
from core.sitemaps import StaticSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('product.urls')),
    path('', include('order.urls')),
    path('', include('user.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
