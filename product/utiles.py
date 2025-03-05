from product.models import Variant, Product


class Collection:
    @staticmethod
    def offers(count=4):
        products = Product.objects.filter(
            discount_percentage__gt=0,
            is_active=True,
            category__is_active=True,
        ).order_by('-discount_percentage')[:count]
        return products
    
    @staticmethod
    def best_sellers(count=4):
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).order_by('-count_sell')[:count]
        return products
    
    @staticmethod
    def new_products(count=4):
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).order_by('-created_at')[:count]
        return products
    
    @staticmethod
    def random_products(count=4):
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).order_by('?')[:count]
        return products
    
    @staticmethod
    def best_viewed(count=4):
        products = Product.objects.filter(
            is_active=True,
            category__is_active=True,
        ).order_by('-count_view')[:count]
        return products

    
