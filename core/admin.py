from django.contrib import admin
from .models import Slider, SiteSettings

# Register your models here.
admin.site.register(Slider)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    search_fields = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    list_filter = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    list_per_page = 10
    
