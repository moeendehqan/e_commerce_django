from core.models import SiteSettings
from order.models import Basket
from django.contrib.auth.models import AnonymousUser  # این خط را اضافه کنید

def site_settings(request):
    return {
        'site_settings': SiteSettings.objects.first(),
    }

def basket_count(request):
    if not hasattr(request, 'user') or isinstance(request.user, AnonymousUser):
        return {'basket_count': 0}  # کاربر احراز هویت نشده است

    return {
        'basket_count': Basket.objects.filter(user=request.user).count(),
    }
