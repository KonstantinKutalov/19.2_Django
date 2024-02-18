import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):
    help = 'Load initial data for categories and products'

    def handle(self, *args, **kwargs):
        with open('categories_fixture.json', 'r', encoding='utf-8') as file:
            categories_data = json.load(file)
        for category_data in categories_data:
            Category.objects.create(name=category_data['name'])

        with open('products_fixture.json', 'r', encoding='utf-8') as file:
            products_data = json.load(file)
        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            Product.objects.create(name=product_data['name'], category=category, attribute1=value1, attribute2=value2)
