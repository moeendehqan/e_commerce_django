from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import Slider, SiteSettings, HomeOption, SmsSetting, Zarinpal, Theme

class SingletonAdmin(admin.ModelAdmin):
    singleton_pk = 1
    def changelist_view(self, request, extra_context=None):
        self.model.get_instance()
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(self.singleton_pk,)))
    def has_add_permission(self, request):
        return not self.model.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        return self.model.objects.filter(pk=self.singleton_pk)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('alt', 'image', 'link', 'active', 'created_at', 'updated_at')
    search_fields = ('alt', 'image', 'link', 'active', 'created_at', 'updated_at')
    list_filter = ('alt', 'image', 'link', 'active', 'created_at', 'updated_at')
    list_per_page = 10

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    search_fields = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    list_filter = ('meta_title', 'meta_description', 'meta_keywords', 'enamad', 'telegram', 'instagram', 'phone', 'email', 'address', 'logo', 'favicon', 'about_us', 'about_us_image', 'telegram_bot', 'contact_us', 'contact_us_image')
    list_per_page = 10
    def changelist_view(self, request, extra_context=None):
        SmsSetting.get_instance()
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(1,)))
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
    def get_queryset(self, request):
        return SiteSettings.objects.filter(pk=1)

@admin.register(SmsSetting)
class SmsSettingAdmin(admin.ModelAdmin):
    fields = ["username", "password", "otp_id", "new_order_id"]
    def changelist_view(self, request, extra_context=None):
        # مطمئن می‌شیم که همیشه یه نمونه با pk=1 وجود داره
        SmsSetting.get_instance()
        # هدایت به صفحه ویرایش رکورد با pk=1
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(1,)))
    def has_add_permission(self, request):
        return not SmsSetting.objects.exists()
    # جلوگیری از حذف رکورد
    def has_delete_permission(self, request, obj=None):
        return False

    # فقط رکورد با pk=1 رو نشون بده (هرچند لیست نمایش داده نمی‌شه)
    def get_queryset(self, request):
        return HomeOption.objects.filter(pk=1)
    
@admin.register(HomeOption)
class HomeOptionAdmin(admin.ModelAdmin):
    # فیلدهایی که توی فرم ادمین نشون داده بشن
    fieldsets = (
            (None, {
                'fields': (
                    'slider',
                    'best_viewed',
                    'best_viewed_count',
                    'new_products',
                    'new_products_count',
                    'best_sellers',
                    'best_sellers_count',
                    'offers',
                    'offers_count',
                    'random_products',
                    'random_products_count',
                ),
                'description': (
                    '<p class="text-blue-600 font-bold">راهنما:</p>'
                    '<p>در این بخش می‌توانید بخش‌های مختلف صفحه اصلی سایت را فعال یا غیرفعال کنید. '
                    'هر گزینه را با دقت انتخاب کنید تا نمایش صفحه اصلی به دلخواه شما تنظیم شود.</p>'
                ),
            }),
        )

    # مخفی کردن لیست رکوردها و هدایت مستقیم به ویرایش
    def changelist_view(self, request, extra_context=None):
        # مطمئن می‌شیم که همیشه یه نمونه با pk=1 وجود داره
        HomeOption.get_instance()
        # هدایت به صفحه ویرایش رکورد با pk=1
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(1,)))

    def has_add_permission(self, request):
        return not HomeOption.objects.exists()

    # جلوگیری از حذف رکورد
    def has_delete_permission(self, request, obj=None):
        return False

    # فقط رکورد با pk=1 رو نشون بده (هرچند لیست نمایش داده نمی‌شه)
    def get_queryset(self, request):
        return HomeOption.objects.filter(pk=1)


@admin.register(Zarinpal)
class ZarinpalAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': (
                    'merchant_id',
                    'token',
                    'sandbox',
                ),
                'description': (
                    '<p class="text-blue-600 font-bold">راهنما:</p>'
                    '<p>در این بخش می‌توانید مشخصات زرین پال را ویرایش کنید.</p>'
                ),
            }),
        )

    def changelist_view(self, request, extra_context=None):
        Zarinpal.get_instance()
        return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(1,)))

    def has_add_permission(self, request):
        return not Zarinpal.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return Zarinpal.objects.filter(pk=1)


@admin.register(Theme)
class ThemeAdmin(SingletonAdmin):
    fieldsets = (
        (None, {
            'fields': ('slider', 'categories_page'),
            'description': (
                '<p class="text-blue-600 font-bold">راهنما:</p>'
                '<p>در این بخش می‌توانید تم اسلایدر و صفحه دسته‌بندی را تنظیم کنید.</p>'
            ),
        }),
    )
    radio_fields = {
        'slider': admin.HORIZONTAL,
        'categories_page': admin.HORIZONTAL,
    }
    def get_queryset(self, request):
        return Theme.objects.filter(pk=1)
    def has_add_permission(self, request):
        return not Theme.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False