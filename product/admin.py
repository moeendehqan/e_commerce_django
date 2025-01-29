from django.contrib import admin
from .models import Category, Product, Variant, VariantImage, Color, Size

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'is_active')
    search_fields = ('name', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords')
    list_per_page = 10



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'image', 'meta_title', 'meta_description', 'meta_keywords', 'category', 'is_active')
    search_fields = ('name', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'category')
    list_filter = ('is_active', 'category')
    list_per_page = 10


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'is_active', 'color', 'size')
    search_fields = ('product', 'name', 'color', 'size')
    list_filter = ('is_active', 'color', 'size')
    list_per_page = 10


@admin.register(VariantImage)
class VariantImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'image')
    search_fields = ('variant', 'image')
    list_filter = ('variant',)
    list_per_page = 10


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code')
    list_per_page = 10


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    list_filter = ('name', 'code')
    list_per_page = 10


