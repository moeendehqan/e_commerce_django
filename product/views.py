from django.shortcuts import  get_object_or_404
from django.views.generic import TemplateView
from .models import Category, Product, Variant, ProductImage
from core.models import SiteSettings
from order.models import Basket

class CategoryListView(TemplateView):
    template_name = 'product/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        meta_tag = {'meta_title': 'دسته بندی ها'}
        context['meta_tag'] = meta_tag
        return context
    
class CategoryDetailView(TemplateView):
    template_name = 'product/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug, is_active=True)
        context['category'] = category
        context['products'] = Product.objects.filter(category=context['category'], is_active=True)
        context['meta_tag'] = {
            'meta_title': 'دسته ' + category.meta_title,
            'meta_description': category.meta_description,
            'meta_keywords': category.meta_keywords,
            'og_image': category.image.url

            }
        return context
    
class ProductDetailView(TemplateView):
    template_name = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug, is_active=True)
        product.count_view += 1
        product.save()
        context['product'] = product
        context['variants'] = Variant.objects.filter(product=product, is_active=True)
        context['default_variant'] = context['variants'].filter(is_default=True).first()  # تنوع پیش‌فرض
        context['product_images'] = ProductImage.objects.filter(product=product)  # تصاویر آلبوم
        context['meta_tag'] = {
            'meta_title': 'محصول ' + product.meta_title,
            'meta_description': product.meta_description,
            'meta_keywords': product.meta_keywords,
            'og_image': product.image.url
            }
        return context