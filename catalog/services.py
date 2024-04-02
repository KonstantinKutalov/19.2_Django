from django.core.cache import cache
from catalog.models import Category


def get_cached_categories():
    cached_categories = cache.get('categories')
    if not cached_categories:
        categories = Category.objects.all()
        cache.set('categories', list(categories), 60 * 10)  # Кешируем на 10 минут
        return categories
    return cached_categories
