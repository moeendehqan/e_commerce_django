from django.contrib import admin
from .models import Category, Product, Variant, ProductImage, Color, Size, Brand, ProductAttribute, ProductAttributeValue

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'parent', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'is_active')
    search_fields = ('name', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords')
    list_per_page = 10



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',  'image', 'meta_title',  'meta_keywords', 'category', 'is_active')
    search_fields = ('name', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'category')
    list_filter = ('is_active', 'category')
    readonly_fields = ('price', 'discount_percentage', 'real_price', 'created_at', 'updated_at')
    list_per_page = 10


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'real_price', 'is_active', 'color', 'size', 'quantity')
    list_editable = ('price', 'real_price', 'is_active', 'quantity')
    search_fields = ('product', 'color', 'size')
    list_filter = ('is_active', 'color', 'size')
    list_per_page = 10
    readonly_fields = ('discount_percentage', 'created_at', 'updated_at')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product', 'image')
    list_filter = ('product',)
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


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug', 'description', 'meta_title', 'meta_description', 'meta_keywords')
    list_per_page = 10


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product', 'attribute', 'value')
    list_per_page = 10

