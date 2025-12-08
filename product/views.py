from django.shortcuts import  get_object_or_404
from django.views.generic import TemplateView
from .models import Category, Product, Variant, ProductImage, ProductAttributeValue
from core.utiles.meta_tag import MetaTag
from core.models import SiteSettings
from core.models import CategorySetting



class CategoryListView(TemplateView):
    template_name = 'categories/categories_classic.html'
    setting = CategorySetting.get_instance()

    def get_template_names(self):
        templates = {
            'classic': 'categories/categories_classic.html',
            'vertical': 'categories/categories_vertical.html',
        }
        return [templates.get(self.setting.theme_categories_page, templates['classic'])]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.filter(is_active=True, parent=None)
        site_settings = SiteSettings.objects.first()
        context['title'] = self.setting.title_categories_page or 'دسته بندی ها'
        meta_tag = MetaTag(title='دسته بندی ها', description=site_settings.meta_description, image=site_settings.logo.url)
        context['meta_tag'] = meta_tag.full_meta_tag()
        return context
    
class CategoryDetailView(TemplateView):
    template_name = 'categories/category_detail.html'
    setting = CategorySetting.get_instance()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug, is_active=True)
        context['category'] = category
        context['subcategories'] = Category.objects.filter(is_active=True, parent=context['category'])
        context['products'] = Product.objects.filter(category=context['category'], is_active=True)
        meta_tag = MetaTag(title= category.meta_title, description=category.meta_description, image=category.image.url)
        context['meta_tag'] = meta_tag.full_meta_tag()
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
        context['attributes'] = ProductAttributeValue.objects.filter(product=product)
        meta_tag = MetaTag(title= product.meta_title, description=product.meta_description, image=product.image.url)
        context['meta_tag'] = meta_tag.full_meta_tag()
        return context