from django.contrib import admin
from .models import Order, Basket, OrderItem


# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_date', 'status')
    search_fields = ('order_number', 'user', 'status')
    list_filter = ('status',)
    list_per_page = 10

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'variant', 'quantity')
    search_fields = ('user', 'variant')
    list_filter = ('user', 'variant')
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variant', 'quantity')
    search_fields = ('order', 'product', 'variant')
    list_filter = ('order', 'product', 'variant')
    list_per_page = 10
    
    


