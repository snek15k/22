from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id):
    cache_key = f'products_in_category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(category_id=category_id, status=Product.STATUS_PUBLISHED).select_related('category')
        cache.set(cache_key, products, 60 * 10)

    return products
