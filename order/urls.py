from django.urls import path
from .views import BasketView, BasketDeleteView, BasketUpdateView, CheckoutView, ZarinpalCallbackView, PaymentSuccessView, PaymentFailedView, OrderTrackingView

app_name = 'order'
urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('basket/<int:variant_id>/', BasketDeleteView.as_view(), name='basket_delete'),
    path('basket/<int:variant_id>/update/', BasketUpdateView.as_view(), name='basket_update'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('zarinpal/callback/', ZarinpalCallbackView.as_view(), name='zarinpal_callback'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', PaymentFailedView.as_view(), name='payment_failed'),
    path('order/tracking/', OrderTrackingView.as_view(), name='order_tracking'),
]
