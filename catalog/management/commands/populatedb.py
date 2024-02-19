import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Product, Category
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Заполнение базы данных новыми данными после очистки старых данных'

    def handle(self, *args, **options):
        self.stdout.write('Очистка старых данных...')
        self.clear_old_data()
        self.stdout.write('Старые данные очищены.')

        self.stdout.write('Заполнение базы данных новыми данными...')
        self.populate_database()
        self.stdout.write('База данных заполнена.')

    def clear_old_data(self):
        with transaction.atomic():
            Product.objects.all().delete()
            Category.objects.all().delete()

    def populate_database(self):
        call_command('loaddata', 'categories_fixture.json')
        call_command('loaddata', 'products_fixture.json')
