from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Slider, SiteSettings
from django.http import HttpResponse
from product.models import Category, Product
from product.utiles import Collection
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm 
from .models import HomeOption
import os
from django.http import FileResponse

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home_settings = HomeOption.get_instance()
        if home_settings.slider:
            context['sliders'] = Slider.objects.filter(active=True)
        if home_settings.offers:
            context['offers'] = Collection.offers(home_settings.offers_count)
        if home_settings.best_viewed:
            context['best_viewed'] = Collection.best_viewed(home_settings.best_viewed_count)
        if home_settings.new_products:
            context['new_products'] = Collection.new_products(home_settings.new_products_count)
        if home_settings.best_sellers:
            context['best_sellers'] = Collection.best_sellers(home_settings.best_sellers_count)
        if home_settings.random_products:
            context['random_products'] = Collection.random_products(home_settings.random_products_count)
        categories = Category.objects.filter(is_active=True)
        if categories.exists():
            context['categories'] = categories
        return context
    
class AboutPage(TemplateView):
    template_name = 'about_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSettings.objects.first()
        context['meta_tag'] = {
            'meta_title': 'درباره ما',
            'meta_description': site_settings.about_us,
            'og_image': site_settings.about_us_image.url
            }
        return context


    
def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Allow: /
"""
    return HttpResponse(content, content_type="text/plain")

def favicon_ico(request):
    site_settings = SiteSettings.objects.first()
    
    if not site_settings or not site_settings.favicon:
        return HttpResponse(status=204)  # No Content
    
    if os.path.exists(site_settings.favicon.path):
        return FileResponse(open(site_settings.favicon.path, 'rb'), content_type='image/x-icon')
    
    # اگه فایل نبود، چیزی برنگردون
    return HttpResponse(status=204)  # No Content



class ContactView(FormView):
    template_name = 'contact_page.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        # ذخیره پیام توی دیتابیس
        contact_message = ContactMessage(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        contact_message.save()
        
        # پیام موفقیت
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد. ما به زودی با شما تماس خواهیم گرفت!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # پیام خطا
        messages.error(self.request, 'لطفاً اطلاعات را به درستی وارد کنید.')
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = SiteSettings.objects.first()
        context['meta_tag'] = {
            'meta_title': 'تماس با ما',
            'meta_description': site_settings.contact_us,
            'og_image': site_settings.contact_us_image.url
            }
        return context
    

class TermsView(TemplateView):
    template_name = 'terms.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_tag'] = {
            'meta_title': 'قوانین و مقررات',
            }
        return context


class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_tag'] = {'meta_title': 'جستجو'}
        return context

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        products = Product.objects.filter(name__icontains=query, is_active=True) if query else []
        context = self.get_context_data(**kwargs)
        context['products'] = products
        context['query'] = query
        return self.render_to_response(context)

    