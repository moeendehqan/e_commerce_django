from django.shortcuts import  get_object_or_404
from django.views.generic import TemplateView
from .models import Category, Product, Variant
from core.models import SiteSettings


class CategoryListView(TemplateView):
    template_name = 'product/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['site_settings'] = SiteSettings.objects.first()
        return context
    
class CategoryDetailView(TemplateView):
    template_name = 'product/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')  # دریافت slug از URL
        context['category'] = get_object_or_404(Category, slug=slug, is_active=True)
        context['site_settings'] = SiteSettings.objects.first()
        context['products'] = Product.objects.filter(category=context['category'], is_active=True) 
        return context
    
class ProductDetailView(TemplateView):
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')  # دریافت slug از URL
        context['product'] = get_object_or_404(Product, slug=slug, is_active=True)
        context['variants'] = Variant.objects.filter(product=context['product'], is_active=True)
        context['site_settings'] = SiteSettings.objects.first()
        return context