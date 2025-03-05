from django.contrib import admin
from .models import Order, Basket, OrderItem, Payment
from zarinpal import ZarinPal
from core.models import SiteSettings
from .utiles import ZarinpalConfig



def inquire_transaction(modeladmin, request, queryset):
    config = ZarinpalConfig()
    zarinpal = ZarinPal(config)
    dic={
        'VERIFIED':'paid',
        'IN_BANK':'pending',
    }
    for payment in queryset:
        if not payment.authority:
            payment.status = 'create error'
            payment.error_message = 'تراکنش فاقد کد یکتا است'
            payment.save()
            continue
        response = zarinpal.inquiries.inquire({
            "authority": payment.authority 
        })
        print(response['data'])
        payment.status = dic[response['data']['status']]
        payment.error_message = None
        payment.code = response['data']['code']
        payment.save()
    modeladmin.message_user(request, "استعلام تراکنش با موفقیت انجام شد")
inquire_transaction.short_description = "استعلام تراکنش"

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
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status','ref_id', 'created_at','error_message')
    search_fields = ('user', 'status')
    list_filter = ('status',)
    list_per_page = 10
    actions = [inquire_transaction]

