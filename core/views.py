from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Slider, SiteSettings
import random
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = random.choice(Slider.objects.all())
        context['site_settings'] = SiteSettings.objects.first()
        return context
    
