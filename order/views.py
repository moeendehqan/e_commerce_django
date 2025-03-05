from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Basket
from product.models import Variant
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .forms import CheckoutForm
from .models import Order, OrderItem, Address, Payment
import uuid
from django.views.generic import FormView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .utiles import ZarinpalConfig
from zarinpal import ZarinPal
from core.models import SiteSettings
import logging
from user.utiles import SendSms


class BasketView(TemplateView):
    template_name = 'basket/basket_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        context['baskets'] = baskets
        total = sum(basket.quantity * basket.variant.real_price for basket in baskets)        
        context['total'] = total
        context['meta_tag'] = {
            'meta_title': 'سبد خرید',
            'robots':'noindex, nofollow'
            }
        return context
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        variant_id = request.POST.get('variant_id')
        variant = Variant.objects.get(id=variant_id)
        quantity = request.POST.get('quantity', 1)

        if not quantity.isdigit() or int(quantity) <= 0:
            quantity = 1

        quantity = int(quantity)

        basket, created = Basket.objects.get_or_create(
            variant=variant, 
            user=user
        )
        if not created:
            basket.quantity += quantity
        else:
            basket.quantity = quantity

        basket.save()
        return redirect('/')
    
class BasketUpdateView(TemplateView):
    @method_decorator(login_required)
    def post(self, request, variant_id):
        variant = Variant.objects.get(id=variant_id)
        quantity = request.POST.get('quantity', 1)
        if not quantity.isdigit() or int(quantity) <= 0:
            quantity = 1
        if int(quantity) > variant.quantity:
            messages.error(request, "تعداد موجودی کالا کمتر از تعداد مورد نظر است")
            return redirect(reverse('basket'))
        quantity = int(quantity)
        basket = Basket.objects.get(variant=variant, user=request.user)
        basket.quantity = quantity
        basket.save()
        return redirect(reverse('basket'))

class BasketDeleteView(TemplateView):
    @method_decorator(login_required)
    def post(self, request, variant_id):
        variant = Variant.objects.get(id=variant_id)
        basket = Basket.objects.get(variant=variant, user=request.user)
        basket.delete()
        return redirect(reverse('basket'))
    



@method_decorator(login_required, name='dispatch')
class CheckoutView(FormView):
    template_name = 'order/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('order:order_success')
    SHIPPING_COST = 30000
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        subtotal = sum(basket.quantity * basket.variant.real_price for basket in baskets)
        total = subtotal + self.SHIPPING_COST
        context['baskets'] = baskets
        context['subtotal'] = subtotal
        context['shipping_cost'] = self.SHIPPING_COST
        context['total'] = total
        context['form'] = CheckoutForm(user=self.request.user)
        context['meta_tag'] = {
            'meta_title': 'پرداخت',
            'robots':'noindex, nofollow'
            }
        return context

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(data=request.POST, user=request.user)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(f"Form errors: {form.errors}")
            return self.form_invalid(form)

    def form_valid(self, form):
        user = self.request.user
        baskets = Basket.objects.filter(user=user)
        
        if not baskets.exists():
            messages.error(self.request, "سبد خرید شما خالی است!")
            return redirect('order:basket')
        
        for basket in baskets:
            if basket.quantity > basket.variant.quantity:
                messages.error(self.request, f"موجودی {basket.variant.product.name} کافی نیست.")
                return redirect('order:basket')
        
        if not Address.objects.filter(user=user).exists():
            messages.error(self.request, "لطفاً ابتدا یک آدرس ثبت کنید.")
            return redirect('order:checkout')

        subtotal = sum(basket.quantity * basket.variant.real_price for basket in baskets)
        count = sum(basket.quantity for basket in baskets)
        total = subtotal + self.SHIPPING_COST
        config = ZarinpalConfig()
        zarinpal = ZarinPal(config)
        payment = Payment(
            user=user,
            amount=total,
        )
        payment.save()
        order = Order(
            user=user,
            payment=payment,
            address=form.cleaned_data['address'],
            shipping_cost=self.SHIPPING_COST,
            total_price=total,
            status='pending'
        )
        order.save()
        total_riyal = int(total)*10
        response = zarinpal.payments.create({
            "amount":total_riyal,
            "callback_url":f"{SiteSettings.objects.all().first().url}/zarinpal/callback/",
            "description":f"پرداخت {total_riyal} ريال برای {count} عدد کالا",
            "mobile":user.mobile if user.mobile else "",
            "email":user.email if user.email else "",
            "referrer_id":order.id,
        })
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            fee = response["data"]["fee"]
            payment_url = zarinpal.payments.generate_payment_url(authority)
        payment.status = 'pending'
        payment.fee = fee
        payment.authority = authority
        payment.save()

        for basket in baskets:
            OrderItem.objects.create(
                order=order,
                product=basket.variant.product,
                variant=basket.variant,
                quantity=basket.quantity
            )
            basket.variant.quantity -= basket.quantity
            basket.variant.save()

        order.total_price = sum(item.variant.price * item.quantity for item in order.items.all())
        order.save()
        return redirect(payment_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class ZarinpalCallbackView(TemplateView):
    def get(self, request, *args, **kwargs):
        status = request.GET.get('Status')
        if status == 'OK':

            authority = request.GET.get('Authority')
            payment = Payment.objects.filter(authority=authority)
            if not payment.exists():
                return redirect('order:payment_failed')
            payment = payment.first()
            config = ZarinpalConfig()
            zarinpal = ZarinPal(config)
            response = zarinpal.verifications.verify({
                    "amount": payment.amount,
                    "authority": authority,
                })
            
            if response["data"]["code"] == 100:
                payment.status = 'paid'
                payment.ref_id = response["data"]["ref_id"]
                payment.card_number = response["data"]["card_pan"]
                payment.card_hash = response["data"]["card_hash"]
                payment.shaparak_fee = response["data"]["shaparak_fee"]
                payment.fee = response["data"]["fee"]
                payment.status = 'paid'
                payment.save()
            baskets = Basket.objects.filter(user=payment.user)
            for basket in baskets:
                product = basket.variant.product
                product.count_sell += basket.quantity
                product.save()
                basket.delete()
            send_sms = SendSms()
            send_sms.send_new_order(payment.user, payment.amount)

            return redirect('order:payment_success')
        else:
            authority = request.GET.get('Authority')
            payment = Payment.objects.filter(authority=authority)
            if not payment.exists():
                return redirect('order:payment_failed')
            payment = payment.first()
            payment.status = 'failed'
            payment.save()
            return redirect('order:payment_failed')


class PaymentSuccessView(TemplateView):
    template_name = 'basket/payment_success.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "پرداخت با موفقیت انجام شد."
        context['meta_tag'] = {
            'meta_title': 'پرداخت موفق',
            'robots':'noindex, nofollow'
            }
        return context

class PaymentFailedView(TemplateView):
    template_name = 'basket/payment_failed.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "پرداخت با مشکل موجود است."
        context['meta_tag'] = {
            'meta_title': 'پرداخت ناموفق',
            'robots':'noindex, nofollow'
            }
        return context


class OrderTrackingView(TemplateView):
    template_name = 'order/order_tracking.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_tag'] = {
            'meta_title': 'پیگیری سفارش',
            'robots':'noindex, nofollow'
            }
        orders = Order.objects.filter(user=self.request.user)
        context['orders'] = orders
        return context
