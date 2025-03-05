from django.urls import path
from .views import HomeView, robots_txt, favicon_ico, AboutPage, ContactView, TermsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('favicon.ico', favicon_ico, name='favicon_ico'),
    path('about/', AboutPage.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('terms/', TermsView.as_view(), name='terms'),
]

