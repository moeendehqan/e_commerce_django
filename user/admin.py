from django.contrib import admin
from .models import User, Otp, Address

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile', 'gender', 'referral_code')
    search_fields = ('username', 'email', 'mobile', 'referral_code')
    list_filter = ('gender', 'referral_code')
    list_per_page = 10

@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('otp', 'mobile', 'is_used')
    search_fields = ('otp', 'mobile')
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'province', 'postal_code')
    search_fields = ('user', 'address', 'city', 'province', 'postal_code')
    list_filter = ('city', 'province', 'postal_code')
    list_per_page = 10

