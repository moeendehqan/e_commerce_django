from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Basket
from product.models import Variant
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

class BasketView(TemplateView):
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
        return redirect('/')  # تغییر مسیر به صفحه‌ای که می‌خواهید



