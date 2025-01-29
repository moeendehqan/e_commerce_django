from django.urls import path
from .views import BasketView
APP_NAME = 'order'
urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
]
